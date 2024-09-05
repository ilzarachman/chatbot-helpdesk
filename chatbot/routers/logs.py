import hashlib
import json
from datetime import datetime
from typing import AsyncGenerator, AsyncIterator

from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect

from chatbot.dependencies.utils.path_utils import project_path
from chatbot.logger import logger
from pydantic import BaseModel
import asyncio
import aiofiles

router = APIRouter(prefix="/logs", tags=["Logs"])


@router.websocket("/connect")
async def websocket_endpoint(websocket: WebSocket):
    """
    Websocket endpoint.

    Args:
        websocket (WebSocket): The websocket.

    Returns:
        dict: The response message.
    """
    try:
        await websocket.accept()

        async def read_logs():
            print("Reading logs...")
            async with aiofiles.open(str(project_path("logs", "app.log.jsonl"))) as f:
                while True:
                    line = await f.readline()
                    if not line:
                        await asyncio.sleep(1)
                        continue
                    log_data = json.loads(line)
                    await websocket.send_text(json.dumps(log_data))

        task = asyncio.create_task(read_logs())

        while True:
            try:
                data = await websocket.receive_text()
                await websocket.send_text(f"Received: {data}")
            except WebSocketDisconnect:
                task.cancel()
                break

    except Exception as e:
        print(f"Error: {e}")
