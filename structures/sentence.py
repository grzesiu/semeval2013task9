from structures.structure import Structure


class Sentence(Structure):
    def __init__(self, _id, text, entities, pairs):
        super().__init__(_id)
        self.text = text
        self.entities = entities
        self.pairs = pairs

    @classmethod
    def parse(cls, node):
        pass
