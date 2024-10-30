from app.services.board_service import GenerationService
from django.shortcuts import render

from app.services.rule_service import RuleService
from app.valueObjects.view_board import ViewBoard, ViewRule


def home(request):
    return render(request, 'home.html')


def show(request):
    service = GenerationService()
    rule_service = RuleService()
    sectors = service.generate()
    start_rules = rule_service.generate_start_rules(sectors)
    conference_rules = rule_service.generate_conferences(sectors, start_rules)
    view_board = ViewBoard.create_from(sectors, 0)

    return render(request, 'game.html', {
        'board': view_board,
        'start_rules': [ViewRule.create_from(rule, sectors) for rule in start_rules],
        'conference_rules': [ViewRule.create_from(rule, sectors, origin, False)
                             for origin, rule in conference_rules.all().items()],
    })


def create(request):
    return render(request, 'home.html')


def move(request):
    return render(request, 'home.html')


def delete(request):
    return render(request, 'home.html')
