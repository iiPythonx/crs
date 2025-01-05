# Copyright (c) 2024-2025 iiPython

__version__ = "0.1.0"

# Modules
import typing
from pathlib import Path
from importlib import util

# Handle routing
class Routing:
    def __init__(self) -> None:
        self.table: dict[str, typing.Any] = {}
        self._current_module: typing.Optional[str] = None

    # Setup methods
    def method(self, method_name: str) -> typing.Callable:
        def inner_callback(function: typing.Callable) -> None:
            if self._current_module is None:
                raise RuntimeError("no module")

            segments = [self._current_module, *method_name.split("/")]
            current_table = self.table
            for index, item in enumerate(segments):
                if item not in current_table:
                    current_table[item] = {}
                    if index == len(segments) - 1:
                        current_table[item] = function
                        break

                current_table = current_table[item]

        return inner_callback

    def build_methods_from_file(self, method_file: Path) -> None:
        module_name = method_file.parent.name
        if method_file.name != "__init__.py":
            module_name += f".{method_file.with_suffix('').name}"

        print(f"Adding module {module_name}")
        # print("BE", self.table)
        self._current_module = module_name
        file_spec = util.spec_from_file_location(module_name, method_file)
        file_spec.loader.exec_module(util.module_from_spec(file_spec))  # pyright: ignore
        self._current_module = None
        # print("AF", self.table)

routing = Routing()
method = routing.method
