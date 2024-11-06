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

    def score(self) -> int:
        match self:
            case Luminary.ASTEROID:
                return 3
            case Luminary.MOON:
                return 2
            case Luminary.NEBULA:
                return 4
            case Luminary.DWARF_PLANET:
                return 4
            case Luminary.PLANET_X:
                return 10
            case _:
                return 0

    def identifier(self) -> str:
        match self:
            case Luminary.ASTEROID:
                return 'ASTEROID'
            case Luminary.MOON:
                return 'MOON'
            case Luminary.NEBULA:
                return 'NEBULA'
            case Luminary.DWARF_PLANET:
                return 'DWARF_PLANET'
            case Luminary.PLANET_X:
                return 'PLANET_X'
            case Luminary.EMPTY_SPACE:
                return 'EMPTY_SPACE'
            case _:
                return 'NONE'

    def appears_as_empty_space(self) -> bool:
        return Luminary.EMPTY_SPACE in self or Luminary.PLANET_X in self

    def is_unfilled(self) -> bool:
        return not bool(self)

    @staticmethod
    def fill_with_all() -> 'Luminary':
        return (Luminary.ASTEROID
                | Luminary.MOON
                | Luminary.NEBULA
                | Luminary.DWARF_PLANET
                | Luminary.PLANET_X
                | Luminary.EMPTY_SPACE)

    def __str__(self):
        return str(luminary.to_string() for luminary in Luminary if luminary in self)

    @staticmethod
    def options() -> dict[int, str]:
        return {option.value: (option.name if option.name else 'None') for option in list(Luminary)}

    @staticmethod
    def from_string(string: str) -> 'Luminary':
        match string:
            case Luminary.MOON.name:
                return Luminary.MOON
            case Luminary.DWARF_PLANET.name:
                return Luminary.DWARF_PLANET
            case Luminary.ASTEROID.name:
                return Luminary.ASTEROID
            case Luminary.NEBULA.name:
                return Luminary.NEBULA
            case Luminary.PLANET_X.name:
                return Luminary.PLANET_X
            case _:
                return Luminary.EMPTY_SPACE

