from django.urls import path
from practice import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dogs/", views.dogs, name="dogs"),
    path("pokemon/", views.team, name="team"),
    path("pokemon/add/", views.add_pokemon, name="add_pokemon"),
    path("pokemon/remove/", views.remove_pokemon, name="remove_pokemon"),
    path("pokemon/search/", views.search_pokemon, name="search_pokemon"),
    path("pokemon/battle/", views.battle, name="battle"),
]
