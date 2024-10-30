from random import choice

from unittest import TestCase

from app.valueObjects.rules import InSectorRule, NotInSectorRule, NextToRule, NotNextToRule, CountInSectorsRule, \
    BandOfSectorsRule
from app.valueObjects.sectors import Sectors
from app.valueObjects.luminary import Luminary


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
        assert valid_rule.valid(board) is None
        invalid_rule = InSectorRule(Luminary.MOON, 5)
        assert invalid_rule.valid(board) == "Moon is not in sector 6.", f"mismatched string: {invalid_rule.valid(board)}"

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
        assert valid_rule.valid(board) is None
        invalid_rule = NotInSectorRule(Luminary.MOON, 10)
        assert invalid_rule.valid(board) == "Moon is in sector 11.", f"mismatched string: {invalid_rule.valid(board)}"

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
        assert valid_rule.valid(board) is None
        invalid_rule = NextToRule(Luminary.PLANET_X, Luminary.EMPTY_SPACE)
        assert invalid_rule.valid(
            board) == "Planet x is not next to Empty space.", f"mismatched string: {invalid_rule.valid(board)}"

    def test_not_next_to_rule(self):
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
        assert valid_rule.valid(board) is None
        invalid_rule = NotNextToRule(Luminary.MOON, Luminary.DWARF_PLANET)
        assert invalid_rule.valid(board) == "Moon is next to Planet.", f"mismatched string: {invalid_rule.valid(board)}"

    def test_count_in_sectors_rule(self):
        board = Sectors().fill({
            0: Luminary.NEBULA,
            1: Luminary.EMPTY_SPACE,
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

        valid_rule = CountInSectorsRule(Luminary.EMPTY_SPACE, 9, 2, 2)
        assert valid_rule.valid(board) is None
        invalid_rule = CountInSectorsRule(Luminary.NEBULA, 7, 11, 2)
        assert invalid_rule.valid(
            board) == "Between sectors 8 and 12, there are not 2 Nebula.", f"mismatched string: {invalid_rule.valid(board)}"

    def test_band_of_n_rule(self):
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
        # assert valid_rule.valid(board) is None
        invalid_rule = BandOfSectorsRule(Luminary.EMPTY_SPACE, 5)
        assert invalid_rule.valid(board) == "Not all Empty space are within 5 sectors.", f"mismatched string: {invalid_rule.valid(board)}"
