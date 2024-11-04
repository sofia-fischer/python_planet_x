from django.shortcuts import redirect, render

from app.models import Board, Game
from app.services.rule_service import RuleService
from app.valueObjects.luminary import Luminary
from app.valueObjects.sectors import Sectors
from app.valueObjects.view_board import ViewBoard, ViewRule


def home(request):
    return render(request, 'home.html')


def show(request, game_id: str):
    game = Game.where_identifier(game_id)
    base_rules = [ViewRule.create_from(rule, 'Base Rule') for rule in RuleService().get_base_rules()]
    learned_rules = [ViewRule.create_from(rule.get_rule(), rule.origin) for rule in game.get_rules()]
    theories = [ViewRule.create_from_theory(rule, game.time_count) for rule in game.get_theories()]
    return render(request, 'game.html', {
        'game_id': game_id,
        'board': ViewBoard.create_from(game.get_notes(), game.time_count),
        'rules': base_rules + learned_rules + theories,
    })


def create(request):
    game = Game.create_game()
    Board.create_board(game)
    rules = []
    for _ in range(0, 5):
        rules.append(RuleService().generate_start_rule(game.get_sectors(), rules))
    [game.add_rule(rule, 'Initial') for rule in rules]
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
    rules = [rule.get_rule() for rule in game.get_rules()]
    game.add_rule(RuleService().generate_conference_rule(game.get_sectors(), rules), 'Conference')
    game.add_time(1)
    _save_notes(request, game)
    return redirect('game_show', game_id)


def target(request, game_id: str):
    game = Game.where_identifier(game_id)
    game.add_rule(RuleService.get_valid_in_sector_rule(game.get_sectors(), int(request.POST.get('target'))), 'Target')
    game.add_time(4)
    _save_notes(request, game)
    return redirect('game_show', game_id)


def survey(request, game_id: str):
    game = Game.where_identifier(game_id)
    start = int(request.POST.get('survey_start'))
    end = int(request.POST.get('survey_end'))

    match request.POST.get('survey_icon'):
        case Luminary.MOON.name:
            icon = Luminary.MOON
        case Luminary.DWARF_PLANET.name:
            icon = Luminary.DWARF_PLANET
        case Luminary.ASTEROID.name:
            icon = Luminary.ASTEROID
        case Luminary.NEBULA.name:
            icon = Luminary.NEBULA
        case _:
            icon = Luminary.EMPTY_SPACE

    game.add_rule(RuleService.get_valid_count_in_sector_rule(game.get_sectors(), icon, start, end), 'Survey')
    absolut_end = end if end >= start else end + Sectors.COUNT
    game.add_time(3 if absolut_end - start <= 3 else 4)
    _save_notes(request, game)
    return redirect('game_show', game_id)


def theory(request, game_id: str):
    game = Game.where_identifier(game_id)
    sector = int(request.POST.get('theory_sector'))

    match request.POST.get('theory_icon'):
        case Luminary.MOON.name:
            icon = Luminary.MOON
        case Luminary.DWARF_PLANET.name:
            icon = Luminary.DWARF_PLANET
        case Luminary.ASTEROID.name:
            icon = Luminary.ASTEROID
        case Luminary.NEBULA.name:
            icon = Luminary.NEBULA
        case _:
            icon = Luminary.EMPTY_SPACE

    game.add_theory(icon, sector)
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
