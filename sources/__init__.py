import importlib
import inspect
import pkgutil
from abc import ABC, abstractmethod
from pathlib import Path

class BaseSource(ABC):
    output_file: str
    @abstractmethod
    def generate(self) -> int:
        pass

SOURCES = []

_package_path = Path(__file__).parent
for _module_info in pkgutil.iter_modules([str(_package_path)]):
    if _module_info.name.startswith("_"):
        continue
    _module = importlib.import_module(f".{_module_info.name}", __package__)
    for _name, _cls in inspect.getmembers(_module, inspect.isclass):
        if _cls.__module__ != _module.__name__:
            continue
        if _name.startswith("_"):
            continue
        if issubclass(_cls, ABC) and bool(_cls.__abstractmethods__):
            continue
        SOURCES.append(_cls())