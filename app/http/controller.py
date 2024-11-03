from django.urls import reverse

from app.models import Game, Board
from django.shortcuts import render, redirect

from app.services.board_service import GenerationService
from app.services.rule_service import RuleService
from app.valueObjects.view_board import ViewBoard, ViewRule


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
        'visibilities': board.get_sector_visibilities().items()
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
    rule = RuleService().generate_conference_rule(game.get_sectors(), game.get_rules())
    game.add_rule(rule, 'Conference')
    game.add_time(1)
    return redirect('game_show', game_id)


def delete(request):
    return render(request, 'home.html')
