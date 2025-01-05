# Copyright (c) 2024-2025 iiPython

# Modules
import sys
import time
import asyncio
from pathlib import Path

import il
import orjson
from pydantic import ValidationError
from websockets.asyncio.server import ServerConnection, serve

from crs import routing, __version__

# Start
il.box(38, f"CRS {__version__}", "(c) iiPython")

async def connect(websocket: ServerConnection) -> None:
    async for message in websocket:
        message = orjson.loads(message)
        start_time = time.perf_counter()

        # Handle routing
        path = message["path"]
        route_match = routing.table.get(path.lstrip("/"))
        if route_match is None:
            await websocket.send(orjson.dumps({"type": "fail", "code": "no_route"}))
            il.request(path, websocket.remote_address[0], "× NO ROUTE", 31, time.perf_counter() - start_time)
            continue

        try:
            await websocket.send(orjson.dumps({
                "type": "success",
                "data": await route_match["func"](route_match["type"](**message["data"]))
            }))
            il.request(path, websocket.remote_address[0], "✓ OK", 32, time.perf_counter() - start_time)

        except ValidationError as e:
            await websocket.send(orjson.dumps({"type": "fail", "code": "validation", "data": e.errors()}))
            il.request(path, websocket.remote_address[0], "× DATA ERROR", 31, time.perf_counter() - start_time)

async def main() -> None:
    async with serve(connect, "localhost", 8765) as socket:
        await socket.serve_forever()

if __name__ == "__main__":

    # Handle method loading
    method_location = Path(__file__).parents[1] / "modules"
    if "--live" in sys.argv:

        # from watchdog.observers import Observer
        # from watchdog.events import FileSystemEvent, FileSystemEventHandler

        # class MyEventHandler(FileSystemEventHandler):
        #     def on_any_event(self, event: FileSystemEvent) -> None:
        #         print(event)

        # event_handler = MyEventHandler()
        # observer = Observer()
        # observer.schedule(event_handler, method_location, recursive = True)
        # observer.start()
        pass

    for file in method_location.rglob("*/*.py"):
        routing.build_methods_from_file(file)

    # Launch websocket
    il.rule(38)
    asyncio.run(main())
