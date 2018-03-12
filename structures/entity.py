from enum import Enum

from structures.structure import Structure


class EntityType(Enum):
    drug = 1
    brand = 2
    group = 3
    no_human = 4


class Entity(Structure):
    def __init__(self, _id, char_offset, entity_type, text):
        self._id = _id
        self.char_offset = char_offset
        self.entity_type = entity_type
        self.text = text

    def parse(self):
        pass
