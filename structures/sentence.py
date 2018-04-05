from structures.entity import Entity, Offset
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
        return Sentence(id_, text, entities, pairs)

    def to_iobs(self):
        iobs = []
        previous = 0
        for entity in self.entities:
            iobs.extend(Entity(None,
                               Offset(previous, entity.offset.start - 1),
                               None,
                               self.text[previous:entity.offset.start]).to_iobs())
            iobs.extend(entity.to_iobs())
            previous = entity.offset.end + 1

        iobs.extend(Entity(None,
                           Offset(previous, len(self.text)),
                           None,
                           self.text[previous:len(self.text)]).to_iobs())
        return iobs
