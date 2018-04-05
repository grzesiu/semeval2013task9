from structures.label import Label


class IOB:
    class Label(Label):
        I = 'I'
        O = 'O'
        B = 'B'

    def __init__(self, text, pos_label, iob_label, entity_label=None):
        self.text = text
        self.pos_label = pos_label
        self.iob_label = iob_label
        self.entity_label = entity_label

    def __repr__(self):
        as_repr = '{0} {1} {2}'.format(self.text, self.pos_label, self.iob_label)
        if self.entity_label:
            as_repr += '-{0}'.format(self.entity_label)
        return as_repr
