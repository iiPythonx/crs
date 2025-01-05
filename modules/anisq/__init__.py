# Copyright (c) 2024-2025 iiPython

# Modules
from crs import method
from attrs import define

# Setup routing
@define
class PingModel:
    something: int

@method("ping")
async def method_ping(result: PingModel) -> dict:
    return {"response": "pong"}
