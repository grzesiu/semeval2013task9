import re
from enum import Enum

from structures.iob import IOB
from structures.structure import Structure


class Entity(Structure):
    class Label(Enum):
        drug = 'drug'
        brand = 'brand'
        group = 'group'

        def __str__(self):
            return str(self.value)

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
        return [cls(id_, offset, label, text) for offset in offsets]

    def to_iobs(self):
        def get_iob_label(k):
            if self.label is None:
                return IOB.Label.O
            elif k == 0:
                return IOB.Label.B
            else:
                return IOB.Label.I

        indices = [Offset(m.start(0), m.end(0)) for m in re.finditer(r'\W', self.text)]
        iobs = []
        previous = 0
        i = 0
        for index in indices:
            word = self.text[previous:index.start]
            separator = self.text[index.start:index.end]
            if word.strip():
                iobs.append(IOB(word,
                                Offset(previous + self.offset.start, index.start + self.offset.start),
                                get_iob_label(i),
                                self.label))
            if separator.strip():
                iobs.append(IOB(separator,
                                Offset(index.start + self.offset.start, index.end + self.offset.start),
                                get_iob_label(i),
                                self.label))
            previous = index.end
            i += 1
        if self.text[previous:].strip():
            iobs.append(IOB(self.text[previous:],
                            Offset(previous + self.offset.start, len(self.text) - 1 + self.offset.start),
                            get_iob_label(i),
                            self.label))
        return iobs

    def __repr__(self):
        return ' '.join([self.text, self.label, repr(self.offset)])

    def __str__(self):
        return self.__repr__()


class Offset:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    @classmethod
    def parse(cls, offset_as_str):
        return [cls(*map(int, offset.split('-'))) for offset in offset_as_str.split(';')]

    def __repr__(self):
        return str(self.start) + '-' + str(self.end)
