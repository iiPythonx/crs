# Copyright (c) 2024-2025 iiPython

__version__ = "0.1.0"

# Modules
import typing
from pathlib import Path
from importlib import util

import il

# Handle routing
class Routing:
    def __init__(self) -> None:
        self.table: dict[str, dict[str, typing.Any]] = {}
        self._current_module: typing.Optional[str] = None

    # Setup methods
    def method(self, method_name: str) -> typing.Callable:
        def inner_callback(function: typing.Callable) -> None:
            if self._current_module is None:
                raise RuntimeError("no module")

            self.table[f"{self._current_module}/{method_name}"] = {
                "func": function,
                "type": typing.get_type_hints(function)["request"]
            }

        return inner_callback

    def build_methods_from_file(self, method_file: Path) -> None:
        module_name = method_file.parent.name
        if method_file.name != "__init__.py":
            module_name += f".{method_file.with_suffix('').name}"

        self._current_module = module_name.replace(".", "/")
        file_spec = util.spec_from_file_location(module_name, method_file)
        file_spec.loader.exec_module(util.module_from_spec(file_spec))  # pyright: ignore
        self._current_module = None

        il.indent(f"+ Module loaded: {module_name}", 34)

routing = Routing()
method = routing.method
