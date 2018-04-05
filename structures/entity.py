from enum import Enum

from structures.structure import Structure


class Entity(Structure):
    class Label(Enum):
        drug = 'drug'
        drug_n = 'drug_n'
        brand = 'brand'
        group = 'group'

    def __init__(self, id_, offsets, label, text):
        super().__init__(id_)
        self.offsets = offsets
        self.label = label
        self.text = text

    @classmethod
    def parse(cls, node):
        id_ = node.attrib.get('id')
        offsets = Entity.parse_offsets(node.attrib.get('charOffset'))
        label = Entity.Label(node.attrib.get('type'))
        text = node.attrib.get('text')
        return [cls(id_, offset, label, text) for offset in offsets]

    @staticmethod
    def parse_offsets(offset):
        return [tuple(map(int, offset.split('-'))) for offset in offset.split(';')]
