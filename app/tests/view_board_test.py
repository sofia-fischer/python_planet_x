from unittest import TestCase

from app.services.board_service import GenerationService
from app.valueObjects.sectors import Sectors
from app.valueObjects.luminary import Luminary
from app.valueObjects.view_board import ViewBoard


class ViewBoardTest(TestCase):
    def test_view_board(self) -> None:
        sectors = GenerationService().generate()
        view_board = ViewBoard.create_from(sectors, 3)
        assert view_board.visible_degree() == 0, f"Expected 0, but actual is {view_board.visible_degree()}"
        assert view_board.sectors[0].visible_sky is False, f"Expected False, but actual is {view_board.sectors[0].visible_sky}"
        assert view_board.get_time_percentage() == 18, f"Expected 30, but actual is {view_board.get_time_percentage()}"
        assert len(view_board.left_board()) == 6, "Expected 6, but actual is " + str(len(view_board.left_board()))
        assert len(view_board.right_board()) == 6, "Expected 6, but actual is " + str(len(view_board.right_board()))
