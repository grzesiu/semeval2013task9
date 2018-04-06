import xml

from structures.sentence import Sentence
from structures.structure import Structure


class Document(Structure):
    def __init__(self, id_, sentences):
        super().__init__(id_)
        self.sentences = sentences

    @classmethod
    def parse(cls, node):
        id_ = node.attrib.get('id')
        sentences = [Sentence.parse(child) for child in node]
        return cls(id_, sentences)

    @classmethod
    def from_file(cls, filename):
        tree = xml.etree.ElementTree.parse(filename)
        return cls.parse(tree.getroot())
