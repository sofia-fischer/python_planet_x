from django.test import TestCase

from app.models import Board, Game


class ModelsTest(TestCase):
    def test_crud_game(self) -> None:
        game = Game.create_game()
        self.assertIsNotNone(game.identifier)
        game.save()
        found_game = Game.where_identifier(game.identifier)
        self.assertEqual(game.identifier, found_game.identifier)
        self.assertEqual(game.id, found_game.id)
        found_game.delete()
        try:
            Game.where_identifier(game.identifier)
            raise AssertionError("Game was not deleted")
        except Game.DoesNotExist:
            self.assertTrue(True)

    def test_crud_board(self) -> None:
        game = Game.create_game()
        game.save()
        board = Board.create_board(game)
        self.assertIsNotNone(game.get_sectors())
        self.assertEqual(board.game.id, game.id)
        game.delete()
        try:
            Board.objects.get(id=board.id)
            raise AssertionError("Board was not deleted")
        except Board.DoesNotExist:
            self.assertTrue(True)
