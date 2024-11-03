from django.test import TestCase
from app.models import Game, Board


class ModelsTest(TestCase):
    def test_crud_game(self) -> None:
        game = Game.create_game()
        assert game.identifier is not None
        game.save()
        foundGame = Game.where_identifier(game.identifier)
        assert game.identifier == foundGame.identifier
        assert game.id == foundGame.id
        foundGame.delete()
        try:
            Game.where_identifier(game.identifier)
            assert False
        except Game.DoesNotExist:
            assert True

    def test_crud_board(self) -> None:
        game = Game.create_game()
        game.save()
        board = Board.create_board(game)
        assert game.get_sectors() is not None
        assert board.game.id == game.id
        game.delete()
        try:
            Board.objects.get(id=board.id)
            assert False
        except Board.DoesNotExist:
            assert True
