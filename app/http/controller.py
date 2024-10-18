from django.shortcuts import render


def home(request):
    context = {"content": 'oh well'}
    return render(request, 'home.html', context)
