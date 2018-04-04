from enum import Enum

from structures.structure import Structure


class Label(Enum):
    drug = 'drug'
    brand = 'brand'
    group = 'group'


class Entity(Structure):
    def __init__(self, id_, offsets, label, text):
        super().__init__(id_)
        self.offsets = offsets
        self.label = label
        self.text = text

    @classmethod
    def parse(cls, node):
        id_ = node.attrib.get('id')
        offsets = Offset.parse(node.attrib.get('charOffset'))
        label = node.attrib.get('type')
        text = node.attrib.get('text')
        return Entity(id_, offsets, label, text)

    def __repr__(self):
        return ' '.join(
            [self.text, self.label, *[repr(offset) for offset in self.offsets]])


class Offset:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    @classmethod
    def parse(cls, offset_as_str):
        return [cls(*map(int, offset.split('-'))) for offset in offset_as_str.split(';')]

    def __repr__(self):
        return str(self.start) + '-' + str(self.end)
