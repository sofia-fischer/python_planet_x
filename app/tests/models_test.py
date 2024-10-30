from unittest import TestCase
from app.models import Game


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
