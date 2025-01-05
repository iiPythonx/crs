# Copyright (c) 2024-2025 iiPython

# Modules
from crs import method
from pydantic import BaseModel

# Setup routing
class PingModel2(BaseModel):
    something: int

@method("ping2")
async def method_ping(request: PingModel2) -> dict:
    return {"response": "pong2"}
