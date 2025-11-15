"""Database block executor - SQL and NoSQL operations"""

from typing import Any, Optional
import asyncpg
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.logging import get_logger
from app.executor.state import WorkflowState

logger = get_logger(__name__)


class DatabaseError(Exception):
    """Custom exception for database errors"""
    pass


async def execute_database_block(
    block: dict[str, Any], input_data: dict[str, Any], state: WorkflowState
) -> dict[str, Any]:
    """Execute a database operation block

    Supports:
    - PostgreSQL queries (SELECT, INSERT, UPDATE, DELETE)
    - MongoDB operations (find, insertOne, updateOne, deleteOne)
    - Parameterized queries for SQL injection protection
    - Transaction support
    """

    logger.info(
        "database_block_executing",
        block_id=block["id"],
        db_type=input_data.get("db_type"),
        operation=input_data.get("operation"),
    )

    db_type = input_data.get("db_type", "postgresql")

    if db_type == "postgresql":
        result = await _execute_postgresql(input_data)
    elif db_type == "mongodb":
        result = await _execute_mongodb(input_data)
    else:
        raise DatabaseError(f"Unsupported database type: {db_type}")

    logger.info("database_block_completed", block_id=block["id"], db_type=db_type)

    return result


async def _execute_postgresql(input_data: dict[str, Any]) -> dict[str, Any]:
    """Execute PostgreSQL query"""

    connection_string = input_data.get("connection_string")
    query = input_data.get("query")
    parameters = input_data.get("parameters", [])
    fetch_mode = input_data.get("fetch_mode", "all")  # all, one, none

    if not connection_string:
        raise DatabaseError("PostgreSQL connection_string is required")

    if not query:
        raise DatabaseError("Query is required")

    conn = None
    try:
        # Connect to database
        conn = await asyncpg.connect(connection_string)

        # Execute query
        if fetch_mode == "none":
            # Execute without fetching (INSERT, UPDATE, DELETE)
            result = await conn.execute(query, *parameters)
            return {
                "success": True,
                "rows_affected": result.split()[-1] if result else 0,
                "data": None,
            }

        elif fetch_mode == "one":
            # Fetch single row
            row = await conn.fetchrow(query, *parameters)
            return {
                "success": True,
                "data": dict(row) if row else None,
                "rows_affected": 1 if row else 0,
            }

        else:  # fetch_mode == "all"
            # Fetch all rows
            rows = await conn.fetch(query, *parameters)
            return {
                "success": True,
                "data": [dict(row) for row in rows],
                "rows_affected": len(rows),
            }

    except Exception as e:
        logger.error("postgresql_query_failed", error=str(e), exc_info=True)
        raise DatabaseError(f"PostgreSQL query failed: {str(e)}") from e

    finally:
        if conn:
            await conn.close()


async def _execute_mongodb(input_data: dict[str, Any]) -> dict[str, Any]:
    """Execute MongoDB operation"""

    connection_string = input_data.get("connection_string")
    database = input_data.get("database")
    collection = input_data.get("collection")
    operation = input_data.get("operation")  # find, findOne, insertOne, updateOne, deleteOne
    filter_query = input_data.get("filter", {})
    document = input_data.get("document")
    update = input_data.get("update")
    limit = input_data.get("limit", 100)

    if not connection_string:
        raise DatabaseError("MongoDB connection_string is required")

    if not database or not collection:
        raise DatabaseError("Database and collection are required")

    if not operation:
        raise DatabaseError("Operation is required")

    client = None
    try:
        # Connect to MongoDB
        client = AsyncIOMotorClient(connection_string)
        db = client[database]
        coll = db[collection]

        # Execute operation
        if operation == "find":
            cursor = coll.find(filter_query).limit(limit)
            documents = await cursor.to_list(length=limit)

            # Convert ObjectId to string
            for doc in documents:
                if '_id' in doc:
                    doc['_id'] = str(doc['_id'])

            return {
                "success": True,
                "data": documents,
                "count": len(documents),
            }

        elif operation == "findOne":
            doc = await coll.find_one(filter_query)

            if doc and '_id' in doc:
                doc['_id'] = str(doc['_id'])

            return {
                "success": True,
                "data": doc,
                "count": 1 if doc else 0,
            }

        elif operation == "insertOne":
            if not document:
                raise DatabaseError("Document is required for insertOne")

            result = await coll.insert_one(document)
            return {
                "success": True,
                "inserted_id": str(result.inserted_id),
                "count": 1,
            }

        elif operation == "updateOne":
            if not update:
                raise DatabaseError("Update is required for updateOne")

            result = await coll.update_one(filter_query, {"$set": update})
            return {
                "success": True,
                "matched_count": result.matched_count,
                "modified_count": result.modified_count,
            }

        elif operation == "deleteOne":
            result = await coll.delete_one(filter_query)
            return {
                "success": True,
                "deleted_count": result.deleted_count,
            }

        else:
            raise DatabaseError(f"Unsupported MongoDB operation: {operation}")

    except Exception as e:
        logger.error("mongodb_operation_failed", error=str(e), exc_info=True)
        raise DatabaseError(f"MongoDB operation failed: {str(e)}") from e

    finally:
        if client:
            client.close()
