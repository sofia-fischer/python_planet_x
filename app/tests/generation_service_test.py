from django.test import TestCase
from app.services.board_service import GenerationService
from app.valueObjects.luminary import Luminary
from app.valueObjects.sectors import Sectors


class TestGenerationService(TestCase):
    def test_generate(self) -> None:
        board = GenerationService().generate()

        # Correct counts
        assert sum(luminary == Luminary.PLANET_X for luminary in board.values()) == 1
        assert sum(luminary == Luminary.MOON for luminary in board.values()) == 2
        assert sum(luminary == Luminary.PLANET for luminary in board.values()) == 1
        assert sum(luminary == Luminary.NEBULA for luminary in board.values()) == 2
        assert sum(luminary == Luminary.EMPTY_SPACE for luminary in board.values()) == 2
        assert sum(luminary == Luminary.ASTEROID for luminary in board.values()) == 4

        # Correct Constraints
        for index, luminary in board.sectors.items():
            if luminary == Luminary.PLANET:
                assert board[(index - 1) % Sectors.COUNT] != Luminary.PLANET_X
                assert board[(index + 1) % Sectors.COUNT] != Luminary.PLANET_X
            if luminary == Luminary.NEBULA:
                assert (board[(index + 1) % Sectors.COUNT] == Luminary.EMPTY_SPACE
                        or board[(index - 1) % Sectors.COUNT] == Luminary.EMPTY_SPACE)
            if luminary == Luminary.MOON:
                assert index in GenerationService.POSSIBLE_MOON_SECTORS
            if luminary == Luminary.ASTEROID:
                assert (board[(index + 1) % Sectors.COUNT] == Luminary.ASTEROID
                        or board[(index - 1) % Sectors.COUNT] == Luminary.ASTEROID)
