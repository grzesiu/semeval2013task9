from abc import ABC, abstractmethod


class Structure(ABC):
    def __init__(self, id_):
        self.id_ = id_

    @classmethod
    @abstractmethod
    def parse(cls, node):
        pass
