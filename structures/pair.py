from enum import Enum

from structures.structure import Structure


class PairType(Enum):
    advice = 'advice'
    effect = 'effect'
    mechanism = 'mechanism'


class Pair(Structure):
    def __init__(self, _id, e1, e2, ddi, pair_type):
        super().__init__(_id)
        self.e1 = e1
        self.e2 = e2
        self.ddi = ddi
        self.pair_type = pair_type

    @classmethod
    def parse(cls, node):
        pass
