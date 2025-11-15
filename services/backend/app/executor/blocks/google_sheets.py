"""Google Sheets block executor - Spreadsheet data management"""

from typing import Any, Optional
import os
import httpx

from app.core.logging import get_logger
from app.executor.state import WorkflowState

logger = get_logger(__name__)


async def execute_google_sheets_block(
    block: dict[str, Any], input_data: dict[str, Any], state: WorkflowState
) -> dict[str, Any]:
    """
    Execute a Google Sheets block for spreadsheet operations

    Supports:
    - Read ranges (get values)
    - Write ranges (update values)
    - Append rows
    - Clear ranges
    - Create spreadsheets
    - Get spreadsheet metadata
    - Batch operations
    """

    logger.info("google_sheets_block_executing", block_id=block["id"], action=input_data.get("action", "read_range"))

    # Get Google Sheets access token (OAuth2)
    access_token = input_data.get("access_token") or input_data.get("google_token") or os.getenv("GOOGLE_SHEETS_TOKEN")
    if not access_token:
        raise ValueError("Google Sheets access token is required. Set GOOGLE_SHEETS_TOKEN environment variable or provide in block config.")

    # Determine action
    action = input_data.get("action", "read_range").lower()

    try:
        if action == "read_range" or action == "read" or action == "get":
            result = await _read_range(access_token, input_data)
        elif action == "write_range" or action == "write" or action == "update":
            result = await _write_range(access_token, input_data)
        elif action == "append_rows" or action == "append":
            result = await _append_rows(access_token, input_data)
        elif action == "clear_range" or action == "clear":
            result = await _clear_range(access_token, input_data)
        elif action == "create_spreadsheet" or action == "create":
            result = await _create_spreadsheet(access_token, input_data)
        elif action == "get_spreadsheet" or action == "get_metadata":
            result = await _get_spreadsheet(access_token, input_data)
        elif action == "batch_update":
            result = await _batch_update(access_token, input_data)
        elif action == "add_sheet" or action == "create_sheet":
            result = await _add_sheet(access_token, input_data)
        elif action == "delete_sheet":
            result = await _delete_sheet(access_token, input_data)
        else:
            raise ValueError(f"Unknown Google Sheets action: {action}")

        logger.info("google_sheets_block_completed", block_id=block["id"], action=action)
        return {"success": True, **result}

    except Exception as e:
        logger.error("google_sheets_block_failed", block_id=block["id"], error=str(e))
        raise


async def _read_range(access_token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Read values from a range in a Google Sheet"""

    spreadsheet_id = input_data.get("spreadsheet_id")
    range_name = input_data.get("range") or input_data.get("range_name", "Sheet1!A1:Z1000")
    value_render_option = input_data.get("value_render_option", "FORMATTED_VALUE")  # FORMATTED_VALUE, UNFORMATTED_VALUE, FORMULA

    if not spreadsheet_id:
        raise ValueError("Spreadsheet ID is required")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{range_name}",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
            params={"valueRenderOption": value_render_option},
            timeout=30.0,
        )

    if response.status_code != 200:
        raise Exception(f"Google Sheets API error: {response.text}")

    result = response.json()
    values = result.get("values", [])

    return {
        "range": result.get("range"),
        "major_dimension": result.get("majorDimension", "ROWS"),
        "values": values,
        "row_count": len(values),
        "column_count": len(values[0]) if values else 0,
    }


async def _write_range(access_token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Write values to a range in a Google Sheet"""

    spreadsheet_id = input_data.get("spreadsheet_id")
    range_name = input_data.get("range") or input_data.get("range_name")
    values = input_data.get("values")
    value_input_option = input_data.get("value_input_option", "USER_ENTERED")  # USER_ENTERED or RAW

    if not spreadsheet_id or not range_name:
        raise ValueError("Spreadsheet ID and range are required")
    if not values:
        raise ValueError("Values are required")

    # Ensure values is a 2D array
    if not isinstance(values, list):
        values = [[values]]
    elif values and not isinstance(values[0], list):
        values = [values]

    payload = {
        "range": range_name,
        "majorDimension": "ROWS",
        "values": values,
    }

    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{range_name}",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            params={"valueInputOption": value_input_option},
            json=payload,
            timeout=30.0,
        )

    if response.status_code != 200:
        raise Exception(f"Google Sheets API error: {response.text}")

    result = response.json()
    return {
        "spreadsheet_id": result.get("spreadsheetId"),
        "updated_range": result.get("updatedRange"),
        "updated_rows": result.get("updatedRows"),
        "updated_columns": result.get("updatedColumns"),
        "updated_cells": result.get("updatedCells"),
    }


async def _append_rows(access_token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Append rows to the end of a Google Sheet"""

    spreadsheet_id = input_data.get("spreadsheet_id")
    range_name = input_data.get("range") or input_data.get("range_name", "Sheet1")
    values = input_data.get("values")
    value_input_option = input_data.get("value_input_option", "USER_ENTERED")

    if not spreadsheet_id:
        raise ValueError("Spreadsheet ID is required")
    if not values:
        raise ValueError("Values are required")

    # Ensure values is a 2D array
    if not isinstance(values, list):
        values = [[values]]
    elif values and not isinstance(values[0], list):
        values = [values]

    payload = {
        "range": range_name,
        "majorDimension": "ROWS",
        "values": values,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{range_name}:append",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            params={"valueInputOption": value_input_option},
            json=payload,
            timeout=30.0,
        )

    if response.status_code != 200:
        raise Exception(f"Google Sheets API error: {response.text}")

    result = response.json()
    updates = result.get("updates", {})

    return {
        "spreadsheet_id": result.get("spreadsheetId"),
        "table_range": result.get("tableRange"),
        "updated_range": updates.get("updatedRange"),
        "updated_rows": updates.get("updatedRows"),
        "updated_columns": updates.get("updatedColumns"),
        "updated_cells": updates.get("updatedCells"),
    }


async def _clear_range(access_token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Clear values from a range in a Google Sheet"""

    spreadsheet_id = input_data.get("spreadsheet_id")
    range_name = input_data.get("range") or input_data.get("range_name")

    if not spreadsheet_id or not range_name:
        raise ValueError("Spreadsheet ID and range are required")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{range_name}:clear",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            json={},
            timeout=30.0,
        )

    if response.status_code != 200:
        raise Exception(f"Google Sheets API error: {response.text}")

    result = response.json()
    return {
        "spreadsheet_id": result.get("spreadsheetId"),
        "cleared_range": result.get("clearedRange"),
    }


async def _create_spreadsheet(access_token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Create a new Google Spreadsheet"""

    title = input_data.get("title") or input_data.get("name", "New Spreadsheet")
    sheets = input_data.get("sheets")  # List of sheet configs

    payload = {
        "properties": {
            "title": title,
        }
    }

    if sheets:
        payload["sheets"] = sheets

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://sheets.googleapis.com/v4/spreadsheets",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30.0,
        )

    if response.status_code not in [200, 201]:
        raise Exception(f"Google Sheets API error: {response.text}")

    spreadsheet = response.json()
    return {
        "spreadsheet_id": spreadsheet.get("spreadsheetId"),
        "spreadsheet_url": spreadsheet.get("spreadsheetUrl"),
        "title": spreadsheet.get("properties", {}).get("title"),
        "sheets": [
            {
                "sheet_id": sheet.get("properties", {}).get("sheetId"),
                "title": sheet.get("properties", {}).get("title"),
            }
            for sheet in spreadsheet.get("sheets", [])
        ],
    }


async def _get_spreadsheet(access_token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Get spreadsheet metadata"""

    spreadsheet_id = input_data.get("spreadsheet_id")
    include_grid_data = input_data.get("include_grid_data", False)

    if not spreadsheet_id:
        raise ValueError("Spreadsheet ID is required")

    params = {}
    if include_grid_data:
        params["includeGridData"] = "true"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
            params=params,
            timeout=30.0,
        )

    if response.status_code != 200:
        raise Exception(f"Google Sheets API error: {response.text}")

    spreadsheet = response.json()
    return {
        "spreadsheet_id": spreadsheet.get("spreadsheetId"),
        "title": spreadsheet.get("properties", {}).get("title"),
        "locale": spreadsheet.get("properties", {}).get("locale"),
        "time_zone": spreadsheet.get("properties", {}).get("timeZone"),
        "sheets": [
            {
                "sheet_id": sheet.get("properties", {}).get("sheetId"),
                "title": sheet.get("properties", {}).get("title"),
                "index": sheet.get("properties", {}).get("index"),
                "sheet_type": sheet.get("properties", {}).get("sheetType"),
                "grid_properties": sheet.get("properties", {}).get("gridProperties"),
            }
            for sheet in spreadsheet.get("sheets", [])
        ],
    }


async def _batch_update(access_token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Execute batch updates on a spreadsheet"""

    spreadsheet_id = input_data.get("spreadsheet_id")
    requests = input_data.get("requests")

    if not spreadsheet_id:
        raise ValueError("Spreadsheet ID is required")
    if not requests:
        raise ValueError("Requests array is required")

    payload = {
        "requests": requests,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}:batchUpdate",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30.0,
        )

    if response.status_code != 200:
        raise Exception(f"Google Sheets API error: {response.text}")

    result = response.json()
    return {
        "spreadsheet_id": result.get("spreadsheetId"),
        "replies": result.get("replies", []),
        "updated_spreadsheet": result.get("updatedSpreadsheet"),
    }


async def _add_sheet(access_token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Add a new sheet to a spreadsheet"""

    spreadsheet_id = input_data.get("spreadsheet_id")
    title = input_data.get("title") or input_data.get("sheet_name", "New Sheet")
    row_count = input_data.get("row_count", 1000)
    column_count = input_data.get("column_count", 26)

    if not spreadsheet_id:
        raise ValueError("Spreadsheet ID is required")

    request = {
        "addSheet": {
            "properties": {
                "title": title,
                "gridProperties": {
                    "rowCount": row_count,
                    "columnCount": column_count,
                }
            }
        }
    }

    payload = {
        "requests": [request],
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}:batchUpdate",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30.0,
        )

    if response.status_code != 200:
        raise Exception(f"Google Sheets API error: {response.text}")

    result = response.json()
    reply = result.get("replies", [{}])[0]
    added_sheet = reply.get("addSheet", {}).get("properties", {})

    return {
        "spreadsheet_id": result.get("spreadsheetId"),
        "sheet_id": added_sheet.get("sheetId"),
        "title": added_sheet.get("title"),
    }


async def _delete_sheet(access_token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Delete a sheet from a spreadsheet"""

    spreadsheet_id = input_data.get("spreadsheet_id")
    sheet_id = input_data.get("sheet_id")

    if not spreadsheet_id or sheet_id is None:
        raise ValueError("Spreadsheet ID and sheet_id are required")

    request = {
        "deleteSheet": {
            "sheetId": sheet_id,
        }
    }

    payload = {
        "requests": [request],
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}:batchUpdate",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30.0,
        )

    if response.status_code != 200:
        raise Exception(f"Google Sheets API error: {response.text}")

    result = response.json()
    return {
        "spreadsheet_id": result.get("spreadsheetId"),
        "deleted_sheet_id": sheet_id,
    }
