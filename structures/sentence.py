from enum import Enum

from structures.entity import Entity
from structures.pair import Pair
from structures.structure import Structure
from util import split


class Sentence(Structure):
    def __init__(self, id_, text, entities, pairs):
        super().__init__(id_)
        self.text = text
        self.entities = entities
        self.pairs = pairs

    @classmethod
    def parse(cls, node):
        id_ = node.attrib.get('id')
        text = node.attrib.get('text')
        entities = [entity for child in node.findall('entity') for entity in Entity.parse(child)]
        pairs = [Pair.parse(child) for child in node.findall('pair')]
        return Sentence(id_, text, entities, pairs)

    def to_iob(self):
        iobs = []

        def add(chunk, entity_label):
            def get_iob_label():
                if entity_label is None:
                    return IOB.Label.O
                elif element_no == 1:
                    return IOB.Label.B
                else:
                    return IOB.Label.I

            for element_no, element in enumerate(split(chunk)):
                iobs.append(IOB(element, get_iob_label(), entity_label))

        add(self.text[0:self.entities[0].offset.start], None)
        add(self.text[self.entities[0].offset.start:self.entities[0].offset.end], self.entities[0].label)

        for i in range(1, len(self.entities)):
            add(self.text[self.entities[i - 1].offset.end:self.entities[i].offset.start], None)
            add(self.text[self.entities[i].offset.start:self.entities[i].offset.end], self.entities[i])

        add(self.text[self.entities[-1].offset.end:len(self.text)], None)

        return iobs


class IOB:
    class Label(Enum):
        I = 'I'
        O = 'O'
        B = 'B'

    def __init__(self, text, label, iob_label):
        self.text = text
        self.label = label
        self.iob_label = iob_label
