from app.models import Game, Board
from django.shortcuts import render, redirect
from app.services.rule_service import RuleService
from app.valueObjects.luminary import Luminary
from app.valueObjects.rules import InSectorRule
from app.valueObjects.view_board import ViewBoard, ViewRule, ViewSector


def home(request):
    return render(request, 'home.html')


def show(request, game_id: str):
    game = Game.where_identifier(game_id)
    board = ViewBoard.create_from(game.get_sectors(), game.timeCount)
    base_rules = RuleService().get_base_rules()
    return render(request, 'game.html', {
        'game_id': game_id,
        'board': board,
        'base_rules': [ViewRule.create_from(rule, game.get_sectors(), 'Base Rule') for rule in base_rules],
        'rules': [ViewRule.create_from(rule.get_rule(), game.get_sectors(), rule.origin) for rule in game.get_rules()],
    })


def create(request):
    game = Game.create_game()
    Board.create_board(game)
    rules = []
    for index in range(0, 5):
        rules.append(RuleService().generate_start_rule(game.get_sectors(), rules))
    [game.add_rule(rule, 'Initial') for rule in rules]
    return redirect('game_show', game.identifier)


def search(request):
    identifier = request.POST.get('game_id') or request.GET.get('game_id')
    if not identifier:
        return render(request, 'home.html', {'error': 'Cannot continue a game without an identifier'})
    return redirect('game_show', identifier)


def conference(request, game_id: str):
    game = Game.where_identifier(game_id)
    game.add_rule(RuleService().generate_conference_rule(game.get_sectors(), game.get_rules()), 'Conference')
    game.add_time(1)
    return redirect('game_show', game_id)


def target(request, game_id: str):
    game = Game.where_identifier(game_id)
    game.add_rule(RuleService.get_valid_in_sector_rule(game.get_sectors(), int(request.POST.get('target'))), 'Target')
    game.add_time(4)
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

    if Luminary.PLANET_X in icon:
        icon = Luminary.EMPTY_SPACE

    game.add_rule(RuleService.get_valid_count_in_sector_rule(game.get_sectors(), icon, start, end), 'Survey')
    absolut_end = end if end >= start else end + 12
    game.add_time(3 if absolut_end - start <= 3 else 4)
    return redirect('game_show', game_id)


def delete(request):
    return render(request, 'home.html')
