# Copyright (c) 2024-2025 iiPython

# Modules
from crs import method
from asyncio import sleep
from pydantic import BaseModel

# Setup routing
class PingModel(BaseModel):
    delay: float

@method("ping")
async def method_ping(request: PingModel) -> dict:
    await sleep(request.delay)
    return {"response": "pong"}
