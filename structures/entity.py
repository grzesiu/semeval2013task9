import re
from enum import Enum

from structures.iob import IOB
from structures.structure import Structure


class Label(Enum):
    drug = 'drug'
    brand = 'brand'
    group = 'group'


class Entity(Structure):
    def __init__(self, id_, offset, label, text):
        super().__init__(id_)
        self.offset = offset
        self.label = label
        self.text = text

    @classmethod
    def parse(cls, node):
        id_ = node.attrib.get('id')
        offsets = Offset.parse(node.attrib.get('charOffset'))
        label = node.attrib.get('type')
        text = node.attrib.get('text')
        return [Entity(id_, offset, label, text) for offset in offsets]

    def to_iobs(self):
        def get_iob_label():
            if self.label is None:
                return IOB.Label.O
            elif i == 0:
                return IOB.Label.B
            else:
                return IOB.Label.I

        indices = [Offset(m.start(0), m.end(0)) for m in re.finditer(r'\W', self.text)]
        iobs = []
        previous = 0
        for i, index in enumerate(indices):
            word = self.text[previous:index.start]
            separator = self.text[index.start:index.end]
            if word != '':
                iobs.append(IOB(word,
                                Offset(previous + self.offset.start, index.start + self.offset.start),
                                get_iob_label(),
                                self.label))
            if separator != ' ':
                iobs.append(IOB(separator,
                                Offset(index.start + self.offset.start, index.end + self.offset.start),
                                get_iob_label(),
                                self.label))
            previous = index.end
        if previous < len(self.text):
            iobs.append(self.text[previous:])
        return iobs

    def __repr__(self):
        return ' '.join([self.text, self.label, repr(self.offset)])


class Offset:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    @classmethod
    def parse(cls, offset_as_str):
        return [cls(*map(int, offset.split('-'))) for offset in offset_as_str.split(';')]

    def __repr__(self):
        return str(self.start) + '-' + str(self.end)
