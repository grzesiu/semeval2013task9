from enum import Enum

from structures.structure import Structure


class EntityType(Enum):
    drug = 'drug'
    brand = 'brand'
    group = 'group'


class Entity(Structure):
    def __init__(self, id_, char_offset, entity_type, text):
        super().__init__(id_)
        self.char_offset = char_offset
        self.entity_type = entity_type
        self.text = text

    @classmethod
    def parse(cls, node):
        id_ = node.attrib.get('id')
        char_offset = node.attrib.get('charOffset')
        entity_type = node.attrib.get('type')
        text = node.attrib.get('text')
        return Entity(id_, char_offset, entity_type, text)
