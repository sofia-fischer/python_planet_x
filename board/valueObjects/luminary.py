from enum import Flag, auto


# One Luminary Flag represents a collection of possible values in a bit map.
# Luminary.ASTEROID | Luminary.PLANET == 9
class Luminary(Flag):
    ASTEROID = auto()  # 1
    MOON = auto()  # 2
    NEBULA = auto()  # 4
    PLANET = auto()  # 8
    PLANET_X = auto()  # 16
    EMPTY_SPACE = auto()  # 32

    def appears_empty(self) -> bool:
        return Luminary.EMPTY_SPACE in self or Luminary.PLANET_X in self

    @staticmethod
    def all():
        return Luminary.ASTEROID | Luminary.MOON | Luminary.NEBULA | Luminary.PLANET | Luminary.PLANET_X | Luminary.EMPTY_SPACE
