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

        return iobs

#
# class IOBsCreator:
#     @staticmethod
#     def create(text, entities):
#         iobs = []
#
#         def add(chunk, start, end, entity_label):
#             def get_iob_label():
#                 if entity_label is None:
#                     return IOB.Label.O
#                 elif element_no == 1:
#                     return IOB.Label.B
#                 else:
#                     return IOB.Label.I
#
#             for element_no, element in enumerate(IOBsCreator.split(chunk)):
#                 iobs.append(IOB(element, start, end, entity_label, get_iob_label()))
#
#         add(text[0:entities[0].offset.start], None)
#         add(text[entities[0].offset.start:entities[0].offset.end], entities[0].label)
#
#         for i in range(1, len(entities)):
#             add(text[entities[i - 1].offset.end:entities[i].offset.start], None)
#             add(text[entities[i].offset.start:entities[i].offset.end], entities[i])
#
#         add(text[entities[-1].offset.end:len(text)], None)
#
#         return iobs
#
#     @staticmethod
#     def find_split_indices(text):
#         return [(m.start(0), m.end(0)) for m in re.finditer(r'\W', text)]
