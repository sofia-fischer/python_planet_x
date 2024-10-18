from django.test import TestCase
from app.valueObjects.board import Board
from app.valueObjects.luminary import Luminary


class TestBoard(TestCase):
    def test_set_edge_case_of_empty_band_of_three(self) -> None:
        board = Board().fill({
            0: Luminary(0),
            1: Luminary.MOON,
            2: Luminary(0),
            3: Luminary(0),
            4: Luminary(0),
            5: Luminary.PLANET,
            6: Luminary(0),
            7: Luminary(0),
            8: Luminary(0),
            9: Luminary.PLANET_X,
            10: Luminary.MOON,
            11: Luminary(0),
        })

        assert board.has_band_of_three_unfilled_sectors()
