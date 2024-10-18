from random import shuffle

from board.Exceptions.board_exception import BoardValidationException
from board.valueObjects.luminary import Luminary


class Board:
    SIZE = 12

    def __init__(self):
        self.sectors = {x: Luminary(0) for x in range(self.SIZE)}

    def fill(self, board: dict[int, Luminary]) -> 'Board':
        if board.keys() != self.sectors.keys():
            raise BoardValidationException("Invalid board")
        self.sectors = board
        return self

    def get_single_sectors(self) -> list[int]:
        result: list[int] = []
        for sector, luminary in self.sectors.items():
            predecessor = self.sectors[(sector - 1) % self.SIZE]
            successor = self.sectors[(sector + 1) % self.SIZE]
            if luminary.is_unfilled() and bool(predecessor) and bool(successor):
                result.append(sector)
        return result

    def has_band_of_three_unfilled_sectors(self) -> bool:
        for sector, luminary in self.sectors.items():
            predecessor = self.sectors[(sector - 1) % self.SIZE]
            successor = self.sectors[(sector + 1) % self.SIZE]
            if luminary.is_unfilled() and predecessor.is_unfilled() and successor.is_unfilled():
                return True
        return False

    def get_predecessor(self, sector: int, skip: int = 0) -> Luminary:
        return self.sectors[(sector - 1 + skip) % self.SIZE]

    def get_empty_sectors_shuffled(self) -> list[int]:
        sectors = [index for index, luminary in self.sectors.items() if luminary.is_unfilled()]
        shuffle(sectors)
        return sectors

    def __getitem__(self, key: int) -> Luminary:
        if key not in self.sectors.keys():
            raise BoardValidationException(f"Key {key} not in board")
        return self.sectors[key]

    def __setitem__(self, key: int, value: Luminary) -> None:
        if key not in self.sectors.keys():
            raise BoardValidationException(f"Key {key} not in board")
        self.sectors[key] = value

    def copy(self) -> 'Board':
        return Board().fill(self.sectors.copy())

    def values(self) -> list[Luminary]:
        return list(self.sectors.values())

    def __str__(self) -> str:
        return str({sector: str(luminary) for sector, luminary in self.sectors})
