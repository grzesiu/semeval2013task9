from structures.entity import Entity
from structures.pair import Pair
from structures.structure import Structure


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
        return cls(id_, text, entities, pairs)

    def __repr__(self):
        return self.text
