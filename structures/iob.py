from enum import Enum


class IOB:
    class Label(Enum):
        I = 'I'
        O = 'O'
        B = 'B'

        def __str__(self):
            return str(self.value)

    def __init__(self, text, offset, iob_label, entity_label=None):
        self.text = text
        self.offset = offset
        self.iob_label = iob_label
        self.entity_label = entity_label

    def __str__(self):
        as_str = '{0.text}\t{0.offset.start}\t{0.offset.end}\t|{0.iob_label}'.format(self)
        if self.entity_label:
            as_str += '-' + self.entity_label
        return as_str
