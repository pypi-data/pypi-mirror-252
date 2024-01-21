from dataclasses import dataclass


@dataclass
class GroupEntity:
    name: str
    parent: str