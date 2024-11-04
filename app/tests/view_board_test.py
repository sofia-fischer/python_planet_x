from unittest import TestCase

from app.services.board_service import GenerationService
from app.valueObjects.view_board import ViewBoard


class ViewBoardTest(TestCase):
    def test_view_board(self) -> None:
        sectors = GenerationService().generate()
        view_board = ViewBoard.create_from(sectors, 3)
        self.assertEqual(view_board.visible_degree(), 0)
        self.assertFalse(view_board.sectors[0].visible_sky)
        self.assertEqual(view_board.get_time_percentage(), 18)
        self.assertEqual(len(view_board.left_board()), 6)
        self.assertEqual(len(view_board.right_board()), 6)
