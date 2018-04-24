import nltk

from structures.iob import IOB
from structures.label import Label
from structures.structure import Structure


class Entity(Structure):
    class Label(Label):
        drug = 'drug'
        drug_n = 'drug_n'
        brand = 'brand'
        group = 'group'

    class Offset:
        def __init__(self, start, end):
            self.start = start
            self.end = end

        @classmethod
        def parse(cls, offset_as_str):
            return [cls(*map(int, offset.split('-'))) for offset in offset_as_str.split(';')]

        def __repr__(self):
            return '{0}-{1}'.format(self.start, self.end)

    def __init__(self, id_, offset, label, text):
        super().__init__(id_)
        self.offset = offset
        self.label = label
        self.text = text

    def to_iob(self):

        def get_iob_label(k):
            if self.label is None:
                return IOB.Label.O
            elif k == 0:
                return IOB.Label.B
            else:
                return IOB.Label.I

        words, offsets = list(zip(*list(self.spans())))
        tagged_words = nltk.pos_tag(words)
        iobs = []
        for i in range(len(tagged_words)):
            iobs.append(IOB(tagged_words[i][0], tagged_words[i][1], get_iob_label(i), self.label, offsets[i]))
        return iobs

    def spans(self):
        tokens = nltk.word_tokenize(self.text)
        offset = 0
        for token in tokens:
            offset = self.text.find(token, offset)
            yield token, Entity.Offset(self.offset.start + offset, self.offset.start + offset + len(token) - 1)
            offset += len(token)

    @classmethod
    def parse(cls, node):
        id_ = node.attrib.get('id')
        offsets = Entity.Offset.parse(node.attrib.get('charOffset'))
        label = Entity.Label(node.attrib.get('type'))
        text = node.attrib.get('text')
        return [cls(id_, offset, label, text) for offset in offsets]

    @classmethod
    def empty(cls, text, start, end):
        return cls(None,
                   Entity.Offset(start, end),
                   None,
                   text[start:end + 1])
