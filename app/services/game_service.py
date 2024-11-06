
from app.models import Board, Game, Rule, Theory
from app.services.rule_service import RuleService
from app.services.sector_service import GenerationService
from app.valueObjects.luminary import Luminary
from app.valueObjects.rules import (
    BaseRule,
    PlanetXLocationRule,
)
from app.valueObjects.sectors import Sectors


class GameService:
    @staticmethod
    def create_game() -> Game:
        game = Game.create_game()
        Board.create_board(game, GenerationService().generate())
        rules: list[BaseRule] = []
        for _ in range(0, 5):
            rules.append(RuleService().generate_start_rule(game.get_sectors(), rules))
        [Rule.create(game, 'Initial', rule) for rule in rules]
        return game

    @staticmethod
    def add_survey(game: Game, icon: Luminary, start: int, end: int) -> Game:
        if Luminary.PLANET_X in icon:
            icon = Luminary.EMPTY_SPACE
        absolut_end = end if end >= start else end + Sectors.COUNT
        game.add_time(3 if absolut_end - start <= 3 else 4)
        rule = RuleService.get_valid_count_in_sector_rule(game.get_sectors(), icon, start, end)
        Rule.create(game, 'Survey', rule)
        return game

    @staticmethod
    def add_conference(game: Game) -> Game:
        rules = [rule.get_rule() for rule in game.get_rules()]
        Rule.create(game, 'Conference', RuleService().generate_conference_rule(game.get_sectors(), rules))
        game.add_time(1)
        return game

    @staticmethod
    def add_target(game: Game, sector: int) -> Game:
        rule = RuleService.get_valid_in_sector_rule(game.get_sectors(), sector)
        game.add_time(4)
        Rule.create(game, 'Target', rule)
        return game

    @staticmethod
    def add_theory(game: Game, icon: Luminary, sector: int) -> Game:
        Theory.create_from(game, icon, sector)
        return game

    @staticmethod
    def add_location_guess(game: Game, sector: int, predecessor: Luminary, successor: Luminary) -> Game:
        rule = PlanetXLocationRule(icon=predecessor, sector=sector, other_icon=successor)
        is_valid = rule.valid(game.get_sectors()) is None
        Rule.create(game, '🎉Located Planet X' if is_valid else '❌ Missed Planet X', rule)
        if not is_valid:
            game.add_time(5)
            return game
        # Game won
        game.score = 10
        for theory in game.get_theories():
            game.score += theory.score
        game.score  = game.score + 16 - min(16, game.time_count)
        game.save()
        return game
