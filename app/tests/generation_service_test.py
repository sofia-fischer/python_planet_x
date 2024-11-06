from unittest import TestCase

from app.services.sector_service import GenerationService
from app.valueObjects.luminary import Luminary
from app.valueObjects.sectors import Sectors


class TestGenerationService(TestCase):
    def test_generate(self) -> None:
        board = GenerationService().generate()

        # Correct counts
        self.assertEqual(sum(luminary == Luminary.PLANET_X for luminary in board.values()),  1)
        self.assertEqual(sum(luminary == Luminary.MOON for luminary in board.values()),  2)
        self.assertEqual(sum(luminary == Luminary.DWARF_PLANET for luminary in board.values()),  1)
        self.assertEqual(sum(luminary == Luminary.NEBULA for luminary in board.values()),  2)
        self.assertEqual(sum(luminary == Luminary.EMPTY_SPACE for luminary in board.values()),  2)
        self.assertEqual(sum(luminary == Luminary.ASTEROID for luminary in board.values()),  4)

        # Correct Constraints
        for index, luminary in board.sectors.items():
            if luminary == Luminary.DWARF_PLANET:
                assert board[(index - 1) % Sectors.COUNT] != Luminary.PLANET_X
                assert board[(index + 1) % Sectors.COUNT] != Luminary.PLANET_X
            if luminary == Luminary.NEBULA:
                self.assertTrue(board[(index + 1) % Sectors.COUNT] == Luminary.EMPTY_SPACE
                                or board[(index - 1) % Sectors.COUNT] == Luminary.EMPTY_SPACE)
            if luminary == Luminary.MOON:
                self.assertIn(index, GenerationService.POSSIBLE_MOON_SECTORS)
            if luminary == Luminary.ASTEROID:
                self.assertTrue(board[(index + 1) % Sectors.COUNT] == Luminary.ASTEROID
                        or board[(index - 1) % Sectors.COUNT] == Luminary.ASTEROID)
