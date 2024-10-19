from app.services.board_service import GenerationService
from django.shortcuts import render

from app.valueObjects.view_board import ViewBoard


def home(request):
    return render(request, 'home.html')


def show(request):
    service = GenerationService()
    view_board = ViewBoard.create_from(service.generate(), 0)

    return render(request, 'game.html', {'board': view_board})


def create(request):
    return render(request, 'home.html')


def move(request):
    return render(request, 'home.html')


def delete(request):
    return render(request, 'home.html')
