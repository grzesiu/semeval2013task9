from enum import Enum


class IOB:
    class Label(Enum):
        I = 'I'
        O = 'O'
        B = 'B'

    def __init__(self, text, offset, iob_label, entity_label=None):
        self.text = text
        self.offset = offset
        self.iob_label = iob_label
        self.entity_label = entity_label

    def __repr__(self):
        return ' '.join(map(str, self.__dict__.values()))
