from dataclasses import dataclass
from typing import Any

class DictMixin:
    def __getitem__(self, key) -> Any:
        return self.__dict__[key]
    
    def get(self, key, default=None) -> Any:
        return self.__dict__.get(key, default)

    def dict(self):
        return self.__dict__


@dataclass
class Node(DictMixin):
    pass


@dataclass
class Edge(DictMixin):
    pass
