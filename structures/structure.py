from abc import ABC, abstractmethod


class Structure(ABC):
    def __init__(self, _id):
        self._id = _id

    @classmethod
    @abstractmethod
    def parse(cls, node):
        pass
