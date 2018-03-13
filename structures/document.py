from structures.structure import Structure


class Document(Structure):
    def __init__(self, _id, sentences):
        super().__init__(_id)
        self.sentences = sentences

    @classmethod
    def parse(cls, node):
        pass
