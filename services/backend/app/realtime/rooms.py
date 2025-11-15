"""Room Management for Socket.IO

Handles room-based broadcasting for:
- Workflow execution rooms
- User collaboration rooms
- Organization-wide broadcasts
"""

from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime

from app.core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class Room:
    """Room information"""

    room_id: str
    room_type: str  # "workflow", "execution", "user", "organization"
    members: Set[str] = field(default_factory=set)
    created_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict = field(default_factory=dict)


class RoomManager:
    """Manages Socket.IO rooms and memberships"""

    def __init__(self):
        self._rooms: Dict[str, Room] = {}
        self._sid_to_rooms: Dict[str, Set[str]] = {}  # Track which rooms each SID is in

    def create_room(
        self,
        room_id: str,
        room_type: str,
        metadata: Optional[Dict] = None,
    ) -> Room:
        """Create a new room

        Args:
            room_id: Unique room identifier
            room_type: Type of room (workflow, execution, user, organization)
            metadata: Additional room metadata

        Returns:
            Room: Created room
        """
        if room_id in self._rooms:
            logger.debug("room_already_exists", room_id=room_id)
            return self._rooms[room_id]

        room = Room(
            room_id=room_id,
            room_type=room_type,
            metadata=metadata or {},
        )
        self._rooms[room_id] = room

        logger.info(
            "room_created",
            room_id=room_id,
            room_type=room_type,
        )

        return room

    def join_room(self, sid: str, room_id: str) -> bool:
        """Add a socket to a room

        Args:
            sid: Socket session ID
            room_id: Room to join

        Returns:
            bool: True if successfully joined
        """
        if room_id not in self._rooms:
            logger.warning("room_not_found", room_id=room_id, sid=sid)
            return False

        room = self._rooms[room_id]
        room.members.add(sid)

        # Track rooms for this SID
        if sid not in self._sid_to_rooms:
            self._sid_to_rooms[sid] = set()
        self._sid_to_rooms[sid].add(room_id)

        logger.debug(
            "socket_joined_room",
            sid=sid,
            room_id=room_id,
            members_count=len(room.members),
        )

        return True

    def leave_room(self, sid: str, room_id: str) -> bool:
        """Remove a socket from a room

        Args:
            sid: Socket session ID
            room_id: Room to leave

        Returns:
            bool: True if successfully left
        """
        if room_id not in self._rooms:
            return False

        room = self._rooms[room_id]
        room.members.discard(sid)

        # Update SID tracking
        if sid in self._sid_to_rooms:
            self._sid_to_rooms[sid].discard(room_id)

        logger.debug(
            "socket_left_room",
            sid=sid,
            room_id=room_id,
            members_count=len(room.members),
        )

        # Delete room if empty
        if len(room.members) == 0:
            self.delete_room(room_id)

        return True

    def delete_room(self, room_id: str) -> bool:
        """Delete a room

        Args:
            room_id: Room to delete

        Returns:
            bool: True if deleted
        """
        if room_id not in self._rooms:
            return False

        room = self._rooms[room_id]

        # Remove room from all SID tracking
        for sid in room.members:
            if sid in self._sid_to_rooms:
                self._sid_to_rooms[sid].discard(room_id)

        del self._rooms[room_id]

        logger.info("room_deleted", room_id=room_id)

        return True

    def disconnect_socket(self, sid: str):
        """Remove socket from all rooms

        Args:
            sid: Socket session ID to disconnect
        """
        if sid not in self._sid_to_rooms:
            return

        # Leave all rooms
        rooms_to_leave = list(self._sid_to_rooms[sid])
        for room_id in rooms_to_leave:
            self.leave_room(sid, room_id)

        # Clean up SID tracking
        if sid in self._sid_to_rooms:
            del self._sid_to_rooms[sid]

        logger.debug("socket_disconnected", sid=sid)

    def get_room_members(self, room_id: str) -> Set[str]:
        """Get all members in a room

        Args:
            room_id: Room identifier

        Returns:
            Set[str]: Set of socket session IDs
        """
        if room_id not in self._rooms:
            return set()

        return self._rooms[room_id].members.copy()

    def get_socket_rooms(self, sid: str) -> Set[str]:
        """Get all rooms a socket is in

        Args:
            sid: Socket session ID

        Returns:
            Set[str]: Set of room IDs
        """
        return self._sid_to_rooms.get(sid, set()).copy()

    def get_room(self, room_id: str) -> Optional[Room]:
        """Get room information

        Args:
            room_id: Room identifier

        Returns:
            Optional[Room]: Room if exists
        """
        return self._rooms.get(room_id)

    def list_rooms(self, room_type: Optional[str] = None) -> List[Room]:
        """List all rooms, optionally filtered by type

        Args:
            room_type: Optional room type filter

        Returns:
            List[Room]: List of rooms
        """
        if room_type:
            return [room for room in self._rooms.values() if room.room_type == room_type]
        return list(self._rooms.values())

    # Helper methods for common room patterns

    def get_workflow_room_id(self, workflow_id: str) -> str:
        """Get room ID for a workflow

        Args:
            workflow_id: Workflow identifier

        Returns:
            str: Room ID
        """
        return f"workflow:{workflow_id}"

    def get_execution_room_id(self, execution_id: str) -> str:
        """Get room ID for a workflow execution

        Args:
            execution_id: Execution identifier

        Returns:
            str: Room ID
        """
        return f"execution:{execution_id}"

    def get_user_room_id(self, user_id: str) -> str:
        """Get room ID for a user

        Args:
            user_id: User identifier

        Returns:
            str: Room ID
        """
        return f"user:{user_id}"

    def get_organization_room_id(self, org_id: str) -> str:
        """Get room ID for an organization

        Args:
            org_id: Organization identifier

        Returns:
            str: Room ID
        """
        return f"org:{org_id}"


# Global room manager instance
room_manager = RoomManager()
