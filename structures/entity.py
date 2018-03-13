from enum import Enum

from structures.structure import Structure


class EntityType(Enum):
    drug = 'drug'
    brand = 'brand'
    group = 'group'


class Entity(Structure):
    def __init__(self, _id, char_offset, entity_type, text):
        self._id = _id
        self.char_offset = char_offset
        self.entity_type = entity_type
        self.text = text

    @classmethod
    def parse(cls, node):
        pass
