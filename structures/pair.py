from enum import Enum

from structures.structure import Structure


class PairType(Enum):
    ddi = 1
    advice = 2
    effect = 3
    mechanism = 4


class Pair(Structure):
    def __init__(self, _id, e1, e2, ddi, pair_type):
        self._id = _id
        self.e1 = e1
        self.e2 = e2
        self.ddi = ddi
        self.pair_type = pair_type

    def parse(self):
        pass
