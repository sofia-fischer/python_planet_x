"""
URL configuration for planet_x project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from app.http import controller

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", controller.home, name="home"),
    path("game/create", controller.create, name="game_create"),
    path("game/search", controller.search, name="game_search"),
    path("game/<str:game_id>", controller.show, name="game_show"),
    path("game/<str:game_id>/save", controller.save, name="game_save"),
    path("game/<str:game_id>/conference", controller.conference, name="game_conference"),
    path("game/<str:game_id>/target", controller.target, name="game_target"),
    path("game/<str:game_id>/survey", controller.survey, name="game_survey"),
    path("game/<str:game_id>/theory", controller.theory, name="game_theory"),
    path("game/<str:game_id>/locate", controller.locate, name="game_locate"),

    # Tailwind
    path("__reload__/", include("django_browser_reload.urls")),
]
