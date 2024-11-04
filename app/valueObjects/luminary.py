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
        match self:
            case Luminary.ASTEROID:
                return 'Asteroid'
            case Luminary.MOON:
                return 'Moon'
            case Luminary.NEBULA:
                return 'Nebula'
            case Luminary.DWARF_PLANET:
                return 'Dwarf Planet'
            case Luminary.PLANET_X:
                return 'Planet X'
            case Luminary.EMPTY_SPACE:
                return 'Empty Space'
            case _:
                return 'None'

    def appears_as_empty_space(self) -> bool:
        return Luminary.EMPTY_SPACE in self or Luminary.PLANET_X in self

    def is_unfilled(self) -> bool:
        return not bool(self)

    @staticmethod
    def fill_with_all() -> 'Luminary':
        return Luminary.ASTEROID | Luminary.MOON | Luminary.NEBULA | Luminary.DWARF_PLANET | Luminary.PLANET_X | Luminary.EMPTY_SPACE

    def __str__(self):
        return str(luminary.to_string() for luminary in Luminary if luminary in self)

    @staticmethod
    def options() -> dict[int, str]:
        return {option.value: (option.name if option.name else 'None') for option in list(Luminary)}
