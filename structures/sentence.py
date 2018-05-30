import re
from itertools import groupby

from structures.entity import Entity
from structures.pair import Pair
from structures.structure import Structure


class Sentence(Structure):
    def __init__(self, id_, text, entities, pairs):
        super().__init__(id_)
        self.text = text
        self.entities = entities
        self.pairs = pairs

    def to_iobs(self):
        iobs = []
        previous = 0

        for entity in self.entities:
            text_left = self.text[previous: entity.offset.start]
            if text_left.strip():
                matches = [(m.group(0), m.start(), m.end() - 1) for m in re.finditer(r'\S+', text_left)]
                for word, start, end in matches:
                    iobs.extend(Entity.empty(self.text, previous + start, previous + end).to_iob())

            iobs.extend(entity.to_iob())
            previous = entity.offset.end + 1

        text_left = self.text[previous:len(self.text)]
        if text_left.strip():
            matches = [(m.group(0), m.start(), m.end() - 1) for m in re.finditer(r'\S+', text_left)]
            for word, start, end in matches:
                iobs.extend(Entity.empty(self.text, previous + start, previous + end).to_iob())

        return iobs

    def __repr__(self):
        return self.text

    @classmethod
    def parse(cls, node, test=False):
        id_ = node.attrib.get('id')
        text = node.attrib.get('text')
        entities = [entity for child in node.findall('entity') for entity in Entity.parse(child, test)]
        pairs = [Pair.parse(child) for child in node.findall('pair')]
        return cls(id_, text, entities, pairs)
