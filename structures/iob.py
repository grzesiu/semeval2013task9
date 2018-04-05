from enum import Enum


class IOB:
    class Label(Enum):
        I = 'I'
        O = 'O'
        B = 'B'

    def __init__(self, text, start, end, iob_label, entity_label=None):
        self.chunk = text[start:end]
        self.start = start
        self.end = end
        self.iob_label = iob_label
        self.entity_label = entity_label
