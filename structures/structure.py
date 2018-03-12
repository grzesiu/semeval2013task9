from abc import ABC, abstractmethod


class Structure(ABC):
    @abstractmethod
    def parse(self):
        pass
