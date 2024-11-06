from random import choice, randrange

from app.Exceptions.board_exception import SectorGenerationException
from app.valueObjects.luminary import Luminary
from app.valueObjects.sectors import Sectors


class GenerationService:
    POSSIBLE_MOON_SECTORS = {1, 2, 4, 6, 10}

    def generate(self) -> Sectors:
        sectors = Sectors()

        # So... there are 2.176.782.336 possible boards.
        # In University, I learned multiple algorithms to deal with Constraint satisfaction problems
        # While working I learned, that the moment you have to use those, your problem is too big for a web developer

        # randomly place planet x
        planet_x_index = randrange(0, Sectors.COUNT)
        sectors[planet_x_index] = Luminary.PLANET_X

        # down to 48.828.125 possible boards
        sectors = self.__set_moons(sectors)

        # down to 262.144 possible boards
        sectors = self.__set_planet(sectors)

        # down to 6561 possible boards
        # place empty space in single sector if required or maybe in pairs
        if (len(sectors.get_single_sectors()) == 1
                or sectors.has_band_of_three_unfilled_sectors()
                or randrange(0, 2) == 0):
            sectors = self.__set_nebulae_in_single_and_triplet(sectors)
        else:
            sectors = self.__set_nebulae_in_pairs(sectors)
            sectors = self.__set_nebulae_in_pairs(sectors)

        # all other sectors are filled with asteroids
        for index in sectors.get_empty_sectors_shuffled():
            sectors[index] = Luminary.ASTEROID

        return sectors

    def __set_moons(self, board: Sectors) -> Sectors:
        planet_x_index = [index for index, luminary in board.sectors.items() if luminary == Luminary.PLANET_X][0]
        # randomly place one moon
        allowed_indexes = self.POSSIBLE_MOON_SECTORS - {planet_x_index}
        moon_index1 = choice(tuple(allowed_indexes))
        board[moon_index1] = Luminary.MOON
        allowed_indexes = allowed_indexes - {moon_index1}

        # If both moons are placed two away from the planet x, the dwarf planet can't be placed there.
        # The dwarf planet and one gas cloud are the only icons that can be placed in "Single Sectors"
        if (planet_x_index + 2) % Sectors.COUNT== moon_index1:
            allowed_indexes = allowed_indexes - {(planet_x_index - 2) % Sectors.COUNT}

        if (planet_x_index - 2) % Sectors.COUNT== moon_index1:
            allowed_indexes = allowed_indexes - {(planet_x_index + 2) % Sectors.COUNT}

        moon_index2 = choice(tuple(allowed_indexes))
        board[moon_index2] = Luminary.MOON
        return board

    def __set_planet(self, board: Sectors) -> Sectors:
        # the dwarf planet must be placed in a way such that at most one single sector is created
        # and it can not be placed next to the planet x
        for index in board.get_empty_sectors_shuffled():
            if (board[(index + 1) % Sectors.COUNT] == Luminary.PLANET_X
                    or board[(index - 1) % Sectors.COUNT] == Luminary.PLANET_X):
                continue
            future_board = board.copy()
            future_board[index] = Luminary.DWARF_PLANET
            if len(future_board.get_single_sectors()) > 1:
                continue

            board[index] = Luminary.DWARF_PLANET
            return board
        raise SectorGenerationException("No valid sector for the dwarf planet found: " + str(board))

    def __set_nebulae_in_single_and_triplet(self, board: Sectors) -> Sectors:
        for index in board.get_empty_sectors_shuffled():
            if board[(index + 1) % Sectors.COUNT] or board[(index + 2) % Sectors.COUNT]:
                continue

            future_board = board.copy()
            future_board[index] = Luminary.NEBULA
            future_board[(index + 1) % Sectors.COUNT] = Luminary.EMPTY_SPACE
            future_board[(index + 2) % Sectors.COUNT] = Luminary.NEBULA
            if len(future_board.get_single_sectors()) > 1:
                continue

            board[index] = Luminary.NEBULA
            board[(index + 1) % Sectors.COUNT] = Luminary.EMPTY_SPACE
            board[(index + 2) % Sectors.COUNT] = Luminary.NEBULA
            if len(board.get_single_sectors()) == 1:
                board[board.get_single_sectors()[0]] = Luminary.EMPTY_SPACE
                return board

            for possible_empty_space in board.get_empty_sectors_shuffled():
                future_board = board.copy()
                future_board[possible_empty_space] = Luminary.EMPTY_SPACE
                if len(future_board.get_single_sectors()) > 0:
                    continue

                board[possible_empty_space] = Luminary.EMPTY_SPACE
                return board
        raise SectorGenerationException("No valid sector for the nebula found: " + str(board))

    def __set_nebulae_in_pairs(self, board: Sectors) -> Sectors:
        for index in board.get_empty_sectors_shuffled():
            if board[index] or board[(index + 1) % Sectors.COUNT]:
                continue

            future_board = board.copy()
            future_board[index] = Luminary.NEBULA
            future_board[(index + 1) % Sectors.COUNT] = Luminary.EMPTY_SPACE
            if len(future_board.get_single_sectors()) > 0:
                continue

            switch = randrange(0, 2)
            board[index] = Luminary.NEBULA if switch else Luminary.EMPTY_SPACE
            board[(index + 1) % Sectors.COUNT] = Luminary.EMPTY_SPACE if switch else Luminary.NEBULA
            return board
        raise SectorGenerationException("No valid sector for the nebula in pairs found: " + str(board))
