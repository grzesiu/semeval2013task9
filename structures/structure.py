from abc import ABC, abstractmethod


class Structure(ABC):
    @classmethod
    @abstractmethod
    def parse(cls, node):
        pass
