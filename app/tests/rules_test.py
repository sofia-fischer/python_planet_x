from random import choice
from unittest import TestCase

from app.valueObjects.luminary import Luminary
from app.valueObjects.rules import (
    BandOfSectorsRule,
    CountInSectorsRule,
    InSectorRule,
    NextToRule,
    NotInSectorRule,
    NotNextToRule,
    NotWithinNSectorsRule,
    PlanetXLocationRule,
    WithinNSectorsRule,
)
from app.valueObjects.sectors import Sectors


class TestRules(TestCase):
    def test_in_sector_rule(self) -> None:
        board = Sectors().fill({
            0: choice(list(Luminary)),
            1: choice(list(Luminary)),
            2: choice(list(Luminary)),
            3: choice(list(Luminary)),
            4: choice(list(Luminary)),
            5: Luminary.NEBULA,
            6: choice(list(Luminary)),
            7: choice(list(Luminary)),
            8: choice(list(Luminary)),
            9: choice(list(Luminary)),
            10: choice(list(Luminary)),
            11: choice(list(Luminary)),
        })

        valid_rule = InSectorRule(Luminary.NEBULA, 5)
        self.assertIsNone(valid_rule.valid(board))
        self.assertEqual(valid_rule.description(), "In sector 6 is Nebula.")
        invalid_rule = InSectorRule(Luminary.MOON, 5)
        self.assertEqual(invalid_rule.valid(board), "In sector 6 is no Moon.")

    def test_not_in_sector_rule(self) -> None:
        board = Sectors().fill({
            0: choice(list(Luminary)),
            1: choice(list(Luminary)),
            2: choice(list(Luminary)),
            3: choice(list(Luminary)),
            4: choice(list(Luminary)),
            5: choice(list(Luminary)),
            6: choice(list(Luminary)),
            7: choice(list(Luminary)),
            8: choice(list(Luminary)),
            9: choice(list(Luminary)),
            10: Luminary.MOON,
            11: choice(list(Luminary)),
        })

        valid_rule = NotInSectorRule(Luminary.PLANET_X, 10)
        self.assertIsNone(valid_rule.valid(board))
        self.assertEqual(valid_rule.description(), "In sector 11 is no Planet X.")
        invalid_rule = NotInSectorRule(Luminary.MOON, 10)
        self.assertEqual(invalid_rule.valid(board), "In sector 11 is Moon.")

    def test_next_to_rule(self) -> None:
        board = Sectors().fill({
            0: Luminary.NEBULA,
            1: Luminary.NEBULA,
            2: Luminary.ASTEROID,
            3: Luminary.ASTEROID,
            4: Luminary.ASTEROID,
            5: Luminary.ASTEROID,
            6: Luminary.PLANET_X,
            7: Luminary.NEBULA,
            8: Luminary.MOON,
            9: Luminary.MOON,
            10: Luminary.EMPTY_SPACE,
            11: Luminary.PLANET_X,
        })

        valid_rule = NextToRule(Luminary.PLANET_X, Luminary.NEBULA)
        self.assertIsNone(valid_rule.valid(board))
        self.assertEqual(valid_rule.description(), "Planet X is always next to Nebula.")
        invalid_rule = NextToRule(Luminary.PLANET_X, Luminary.EMPTY_SPACE)
        self.assertEqual(invalid_rule.valid(board), "Planet X is not next to Empty Space.")

    def test_not_next_to_rule(self) -> None:
        board = Sectors().fill({
            0: Luminary.NEBULA,
            1: Luminary.MOON,
            2: Luminary.NEBULA,
            3: Luminary.EMPTY_SPACE,
            4: Luminary.ASTEROID,
            5: Luminary.ASTEROID,
            6: Luminary.ASTEROID,
            7: Luminary.ASTEROID,
            8: Luminary.MOON,
            9: Luminary.DWARF_PLANET,
            10: Luminary.DWARF_PLANET,
            11: Luminary.EMPTY_SPACE,
        })

        valid_rule = NotNextToRule(Luminary.MOON, Luminary.EMPTY_SPACE)
        self.assertIsNone(valid_rule.valid(board))
        self.assertEqual(valid_rule.description(), "Moon is never next to Empty Space.")
        invalid_rule = NotNextToRule(Luminary.MOON, Luminary.DWARF_PLANET)
        self.assertEqual(invalid_rule.valid(board), "Moon is next to Dwarf Planet.")

    def test_count_in_sectors_rule(self) -> None:
        board = Sectors().fill({
            0: Luminary.NEBULA,
            1: Luminary.EMPTY_SPACE,
            2: Luminary.ASTEROID,
            3: Luminary.ASTEROID,
            4: Luminary.ASTEROID,
            5: Luminary.ASTEROID,
            6: Luminary.DWARF_PLANET,
            7: Luminary.NEBULA,
            8: Luminary.MOON,
            9: Luminary.MOON,
            10: Luminary.EMPTY_SPACE,
            11: Luminary.PLANET_X,
        })

        valid_rule = CountInSectorsRule(Luminary.EMPTY_SPACE, 9, 1, 2)
        self.assertIsNone(valid_rule.valid(board))
        self.assertEqual(valid_rule.description(), "There are 2 Empty Space within sector 10 to 2.")
        invalid_rule = CountInSectorsRule(Luminary.NEBULA, 7, 11, 2)
        self.assertEqual(invalid_rule.valid(board), "There are 1 Nebula within sector 8 to 12, but there should be 2.")

    def test_band_of_n_rule(self) -> None:
        board = Sectors().fill({
            0: Luminary.ASTEROID,
            1: Luminary.EMPTY_SPACE,
            2: Luminary.ASTEROID,
            3: Luminary.ASTEROID,
            4: Luminary.PLANET_X,
            5: Luminary.NEBULA,
            6: Luminary.EMPTY_SPACE,
            7: Luminary.NEBULA,
            8: Luminary.MOON,
            9: Luminary.DWARF_PLANET,
            10: Luminary.MOON,
            11: Luminary.ASTEROID,
        })

        valid_rule = BandOfSectorsRule(Luminary.ASTEROID, 5)
        self.assertIsNone(valid_rule.valid(board))
        self.assertEqual(valid_rule.description(), "All Asteroid are within a band of 5 sectors.")
        invalid_rule = BandOfSectorsRule(Luminary.EMPTY_SPACE, 5)
        self.assertEqual(invalid_rule.valid(board), "Not all Empty Space are within 5 sectors.")

    def test_within_rule(self) -> None:
        board = Sectors().fill({
            0: Luminary.EMPTY_SPACE,
            1: Luminary.NEBULA,
            2: Luminary.MOON,
            3: Luminary.ASTEROID,
            4: Luminary.ASTEROID,
            5: Luminary.MOON,
            6: Luminary.PLANET_X,
            7: Luminary.EMPTY_SPACE,
            8: Luminary.ASTEROID,
            9: Luminary.ASTEROID,
            10: Luminary.DWARF_PLANET,
            11: Luminary.NEBULA,
        })

        valid_rule = WithinNSectorsRule(Luminary.ASTEROID, Luminary.NEBULA, 3)
        self.assertIsNone(valid_rule.valid(board))
        self.assertEqual(valid_rule.description(), "Asteroid is always within 3 sectors of Nebula.")
        invalid_rule = WithinNSectorsRule(Luminary.ASTEROID, Luminary.MOON, 3)
        self.assertEqual(invalid_rule.valid(board), "Asteroid is not within 3 sectors of Moon.")

    def test_not_within_rule(self) -> None:
        board = Sectors().fill({
            0: Luminary.EMPTY_SPACE,
            1: Luminary.NEBULA,
            2: Luminary.MOON,
            3: Luminary.ASTEROID,
            4: Luminary.ASTEROID,
            5: Luminary.MOON,
            6: Luminary.PLANET_X,
            7: Luminary.EMPTY_SPACE,
            8: Luminary.ASTEROID,
            9: Luminary.ASTEROID,
            10: Luminary.DWARF_PLANET,
            11: Luminary.NEBULA,
        })

        valid_rule = NotWithinNSectorsRule(Luminary.MOON, Luminary.DWARF_PLANET, 2)
        self.assertIsNone(valid_rule.valid(board))
        self.assertEqual(valid_rule.description(), "Moon is never within 2 sectors of Dwarf Planet.")
        invalid_rule = NotWithinNSectorsRule(Luminary.MOON, Luminary.NEBULA, 3)
        self.assertEqual(invalid_rule.valid(board), "Moon is within 3 sectors of Nebula.")

    def test_locate_planet_x_rule(self) -> None:
        board = Sectors().fill({
            0: Luminary.EMPTY_SPACE,
            1: Luminary.NEBULA,
            2: Luminary.MOON,
            3: Luminary.ASTEROID,
            4: Luminary.ASTEROID,
            5: Luminary.ASTEROID,
            6: Luminary.ASTEROID,
            7: Luminary.DWARF_PLANET,
            8: Luminary.EMPTY_SPACE,
            9: Luminary.PLANET_X,
            10: Luminary.MOON,
            11: Luminary.NEBULA,
        })

        valid_rule = PlanetXLocationRule(Luminary.MOON, 6, Luminary.EMPTY_SPACE)
        self.assertIsNone(valid_rule.valid(board))
        self.assertEqual(valid_rule.description(), "Planet X was located in sector 7 "
                                                   "with Moon as predecessor and Empty Space as successor.")
        invalid_rule = PlanetXLocationRule(Luminary.MOON, 5, Luminary.NEBULA)
        self.assertEqual(invalid_rule.valid(board), "Planet X is NOT correctly located in sector 6 "
                                                    "with Moon as predecessor and Nebula as successor.")

