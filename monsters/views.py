from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from monsters.models import Monster


class DungeonView(LoginRequiredMixin, TemplateView):
    template_name = 'monsters/dungeon.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['monsters'] = Monster.objects.order_by('rating')
        return context


def get_monster_name(slug):
    if slug == "scarab_beetle":
        return "Scarab Beetle"
    elif slug == "evil_mummy":
        return "Evil Mummy"
    elif slug == "anubis":
        return "Anubis"
    elif slug == "judge_the_destroyer":
        return "Judge the Destroyer"


class MonsterFightView(LoginRequiredMixin, View):
    template_name = 'monsters/fight_monster.html'

    def get(self, request, slug):
        try:
            monster = Monster.objects.get(slug=get_monster_name(slug))
        except:
            pass

        character = request.user.character
        # Return character to Tavern to heal.
        if character.health == 0:
            return redirect("character_has_died")
