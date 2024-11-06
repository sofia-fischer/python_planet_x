from django.shortcuts import redirect, render

from app.models import Game
from app.services.game_service import GameService
from app.services.rule_service import RuleService
from app.valueObjects.luminary import Luminary
from app.valueObjects.sectors import Sectors
from app.valueObjects.view_board import ViewBoard, ViewRule


def home(request):
    return render(request, 'home.html')


def show(request, game_id: str):
    game = Game.where_identifier(game_id)
    base_rules = [ViewRule.create_from(rule, 'Base Rule') for rule in RuleService.get_base_rules()]
    learned_rules = [ViewRule.create_from(rule.get_rule(), rule.origin) for rule in game.get_rules()]
    theories = [ViewRule.create_from_theory(rule, game.time_count) for rule in game.get_theories()]
    return render(request, 'game.html', {
        'game_id': game_id,
        'board': ViewBoard.create_from(
            board=game.get_sectors(),
            timer=game.time_count,
            solution=game.get_sectors() if game.score > 0 else None
        ),
        'rules': base_rules + learned_rules + theories,
        'score': game.score,
    })


def create(request):
    game = GameService.create_game()
    return redirect('game_show', game.identifier)


def save(request, game_id: str):
    game = Game.where_identifier(game_id)
    _save_notes(request, game)
    return redirect('game_show', game_id)


def search(request):
    identifier = request.POST.get('game_id') or request.GET.get('game_id')
    if not identifier:
        return render(request, 'home.html', {'error': 'Cannot continue a game without an identifier'})
    return redirect('game_show', identifier)


def conference(request, game_id: str):
    game = Game.where_identifier(game_id)
    GameService.add_conference(game)
    _save_notes(request, game)
    return redirect('game_show', game_id)


def target(request, game_id: str):
    game = Game.where_identifier(game_id)
    GameService.add_target(game, int(request.POST.get('target')))
    _save_notes(request, game)
    return redirect('game_show', game_id)


def survey(request, game_id: str):
    game = Game.where_identifier(game_id)
    GameService.add_survey(
        game = game,
        icon=Luminary.from_string(request.POST.get('survey_icon')),
        start=int(request.POST.get('survey_start')),
        end=int(request.POST.get('survey_end')),
    )
    _save_notes(request, game)
    return redirect('game_show', game_id)


def theory(request, game_id: str):
    game = Game.where_identifier(game_id)
    GameService.add_theory(
        game = game,
        icon = Luminary.from_string(request.POST.get('theory_icon')),
        sector = int(request.POST.get('theory_sector'))
    )
    _save_notes(request, game)
    return redirect('game_show', game_id)


def locate(request, game_id: str):
    game = Game.where_identifier(game_id)
    sector = int(request.POST.get('locate_sector'))
    predecessor = Luminary.from_string(request.POST.get('locate_predecessor'))
    successor = Luminary.from_string(request.POST.get('locate_successor'))
    GameService.add_location_guess(game, sector, predecessor, successor)
    _save_notes(request, game)
    return redirect('game_show', game_id)


def _save_notes(request, game: Game) -> Game:
    if request.POST.get("sector_1_" + Luminary.MOON.identifier()) is None:
        return game
    sectors = {}
    for index in range(0, Sectors.COUNT):
        luminary = Luminary(0)
        for option in Luminary:
            if request.POST.get("sector_" + str(index) + "_" + option.identifier()):
                luminary = luminary | option
        sectors[index] = luminary

    game.set_notes(Sectors().fill(sectors))
    return game


def delete(request):
    return render(request, 'home.html')
