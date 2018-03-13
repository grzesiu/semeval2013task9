from structures.structure import Structure


class Document(Structure):
    def __init__(self, _id, sentences):
        self._id = _id
        self.sentences = sentences

    @classmethod
    def parse(cls, node):
        pass
