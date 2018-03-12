from structures.structure import Structure


class Sentence(Structure):
    def __init__(self, _id, text, entities, pairs):
        self._id = _id
        self.text = text
        self.entities = entities
        self.pairs = pairs

    def parse(self):
        pass
