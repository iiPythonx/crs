# Copyright (c) 2024-2025 iiPython

# Modules
import sys
import asyncio
from pathlib import Path

from websockets.asyncio.server import serve

from crs import routing

# Start
async def connect(websocket) -> None:
    async for message in websocket:
        print(message)

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
    asyncio.run(main())
