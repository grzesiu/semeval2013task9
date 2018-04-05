from enum import Enum


class Label(Enum):
    def __str__(self):
        return self.value
