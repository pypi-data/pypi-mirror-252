from dataclasses import dataclass


@dataclass
class Group:
    name: str
    parent: str