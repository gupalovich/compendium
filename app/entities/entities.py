from dataclasses import dataclass
from uuid import uuid4


@dataclass
class Entity:
    """Base class for all entities"""

    id: str = None

    def __post_init__(self):
        self.id = self.id or str(uuid4())


@dataclass
class Item(Entity):
    """Base class for all items"""

    name: str = None
    description: str = None
