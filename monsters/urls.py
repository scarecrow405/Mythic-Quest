from django.urls import path

from monsters.views import DungeonView, MonsterFightView

urlpatterns = [
    path("dungeon/", DungeonView.as_view(), name="dungeon"),
    path("fight/<slug:slug>/", MonsterFightView.as_view(), name="fight_monster"),
]
