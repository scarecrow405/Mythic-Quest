from django.urls import path

from games.views import earn_gold_by_clicking_game
from home.views import HomeViewWithCharacter, HomeViewWithoutCharacter, ContactViewForm

urlpatterns = [
    path('earn_gold_by_clicking/', earn_gold_by_clicking_game, name='earn_gold_by_clicking'),
]
