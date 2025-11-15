import { io, Socket } from "socket.io-client";

// Assume authStore provides the JWT token
// Example structure (replace with actual store import):
interface AuthState {
  accessToken: string | null;
}

const mockAuthState: AuthState = {
  accessToken: localStorage.getItem("access_token"),
};

// Function to get the token (should be dynamic based on auth store)
function getToken(): string | null {
  return mockAuthState.accessToken;
}

class SocketManager {
  private socket: Socket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;

  constructor() {
    console.log("SocketManager initialized");
  }

  connect() {
    const token = getToken();
    if (!token) {
      console.warn("No auth token found, not connecting to Socket.IO");
      return;
    }

    if (this.socket && this.socket.connected) {
      console.log("Socket already connected");
      return;
    }

    console.log("Attempting to connect to Socket.IO...");
    this.socket = io(import.meta.env.VITE_SOCKET_URL || "http://localhost:8000", {
      path: import.meta.env.VITE_SOCKET_PATH || "/socket.io",
      auth: {
        token: token,
      },
      transports: ["websocket", "polling"],
      reconnection: true,
      reconnectionAttempts: this.maxReconnectAttempts,
      reconnectionDelay: 1000, // Initial delay 1 second
    });

    this.setupEventHandlers();
  }

  private setupEventHandlers() {
    this.socket?.on("connect", () => {
      console.log("✅ Socket connected:", this.socket?.id);
      this.reconnectAttempts = 0;
    });

    this.socket?.on("disconnect", (reason) => {
      console.log("❌ Socket disconnected:", reason);
      if (reason === "io server disconnect") {
        // The disconnection was initiated by the server, cannot force reconnection
        this.socket?.connect();
      }
      // Enable attempting to reconnect unless the reason is "io server disconnect"
    });

    this.socket?.on("connect_error", (error) => {
      console.error("🆘 Socket connection error:", error.message);
      this.reconnectAttempts++;
      if (this.reconnectAttempts >= this.maxReconnectAttempts) {
        console.error("Max reconnection attempts reached. Stopping.");
        this.socket?.disconnect();
      }
    });

    // Add other essential event handlers here (e.g., workflow events, execution events)
    this.socket?.onAny((event, ...args) => {
      console.log(`Received event: ${event}`, args);
    });
  }

  emit(event: string, data: any) {
    if (this.socket && this.socket.connected) {
      this.socket.emit(event, data);
    } else {
      console.warn("Socket not connected, cannot emit event:", event);
    }
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
      console.log("Socket disconnected");
    }
  }

  isConnected(): boolean {
    return this.socket?.connected ?? false;
  }
}

export const socketManager = new SocketManager();

// Helper functions for execution monitoring
export function onSocketEvent(event: string, callback: (...args: any[]) => void) {
  if (socketManager['socket']) {
    socketManager['socket'].on(event, callback);
  }
}

export function offSocketEvent(event: string, callback: (...args: any[]) => void) {
  if (socketManager['socket']) {
    socketManager['socket'].off(event, callback);
  }
}

export function joinExecution(executionId: string) {
  socketManager.emit('join_execution', { execution_id: executionId });
}

export function leaveExecution(executionId: string) {
  socketManager.emit('leave_execution', { execution_id: executionId });
}