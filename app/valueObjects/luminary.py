import string
from enum import Flag, auto


# One Luminary Flag represents a collection of possible values in a bit map.
# Luminary.ASTEROID | Luminary.PLANET == 9
class Luminary(Flag):
    ASTEROID = auto()  # 1
    MOON = auto()  # 2
    NEBULA = auto()  # 4
    DWARF_PLANET = auto()  # 8
    PLANET_X = auto()  # 16
    EMPTY_SPACE = auto()  # 32

    def to_string(self) -> str:
        return self.name.replace('_', ' ').capitalize()

    def appears_as_empty_space(self) -> bool:
        return Luminary.EMPTY_SPACE in self or Luminary.PLANET_X in self

    def is_unfilled(self) -> bool:
        return not bool(self)

    @staticmethod
    def fill_with_all():
        return Luminary.ASTEROID | Luminary.MOON | Luminary.NEBULA | Luminary.DWARF_PLANET | Luminary.PLANET_X | Luminary.EMPTY_SPACE

    def __str__(self):
        return str(luminary.name if luminary else 'None' for luminary in Luminary if luminary in self)

    @staticmethod
    def options() -> [string, int]:
        return [(option.value, option.name) for option in list(Luminary)]
