from enum import Enum

from structures.structure import Structure


class Label(Enum):
    advice = 'advice'
    effect = 'effect'
    mechanism = 'mechanism'


class Pair(Structure):
    def __init__(self, id_, e1, e2, ddi, label):
        super().__init__(id_)
        self.e1 = e1
        self.e2 = e2
        self.ddi = ddi
        self.label = label

    @classmethod
    def parse(cls, node):
        id_ = node.attrib.get('id')
        e1 = node.attrib.get('e1')
        e2 = node.attrib.get('e2')
        ddi = node.attrib.get('ddi')
        label = node.attrib.get('type')
        return Pair(id_, e1, e2, ddi, label)
