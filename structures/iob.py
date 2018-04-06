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
        return '{0} {1} {2}'.format(self.text, self.pos_label, self.get_label())

    def get_label(self):
        label = str(self.iob_label)
        if self.entity_label:
            label += '-' + str(self.entity_label)
        return label
