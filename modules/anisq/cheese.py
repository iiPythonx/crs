# Copyright (c) 2024-2025 iiPython

# Modules
from crs import method
from attrs import define

# Setup routing
@define
class PingModel2:
    something: int

@method("ping2")
async def method_ping(result: PingModel2) -> dict:
    return {"response": "pong2"}
