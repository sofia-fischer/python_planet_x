from django.urls import reverse

from app.models import Game, Board
from django.shortcuts import render, redirect
from app.services.rule_service import RuleService
from app.valueObjects.view_board import ViewBoard, ViewRule


def home(request):
    return render(request, 'home.html')


def show(request, game_id: str):
    game = Game.where_identifier(game_id)
    rule_service = RuleService()
    sectors = game.get_sectors()
    start_rules = rule_service.generate_start_rules(sectors)
    conference_rules = rule_service.generate_conferences(sectors, start_rules)

    return render(request, 'game.html', {
        'game_id': game_id,
        'board': ViewBoard.create_from(sectors, 0),
        'start_rules': [ViewRule.create_from(rule, sectors) for rule in start_rules],
        'conference_rules': [ViewRule.create_from(rule, sectors, origin, False)
                             for origin, rule in conference_rules.all().items()],
    })


def create(request):
    game = Game.create_game()
    Board.create_board(game)
    return redirect('game_show', game.identifier)


def search(request):
    identifier = request.POST.get('game_id') or request.GET.get('game_id')
    if not identifier:
        return render(request, 'home.html', {'error': 'Cannot continue a game without an identifier'})
    return redirect('game_show', identifier)


def move(request):
    return render(request, 'home.html')


def delete(request):
    return render(request, 'home.html')
