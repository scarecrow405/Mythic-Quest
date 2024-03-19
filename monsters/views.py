from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from monsters.models import Monster
from monsters.monster_fight_logic import monster_fight


class DungeonView(LoginRequiredMixin, TemplateView):
    template_name = 'monsters/dungeon.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        for monster in context['monsters']:
            monster.save()

        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['monsters'] = Monster.objects.order_by('rating')
        return context


def get_monster_name(slug):
    if slug == "scarab-beetle":
        return "Scarab Beetle"
    elif slug == "evil-mummy":
        return "Evil Mummy"
    elif slug == "anubis":
        return "Anubis"
    elif slug == "judge-the-destroyer":
        return "Judge the Destroyer"
    return slug


class MonsterFightView(LoginRequiredMixin, View):
    template_name = 'monsters/fight_monster.html'

    def get(self, request, slug):
        character = request.user.character

        monster_name = get_monster_name(slug)
        monster = Monster.objects.filter(name__exact=monster_name).first()

        if monster is None:
            return redirect('error_404')

        if character.health == 0:
            return redirect("character_has_died")

        winner, gained_exp, gained_gold, win_chance, damage_taken = monster_fight(character, monster)

        context = {
            'character': character,
            'monster': monster,
            'winner': winner,
            'gained_gold': gained_gold,
            'gained_exp': gained_exp,
            'win_chance': win_chance,
            'damage_taken': damage_taken
        }

        return render(request, 'monsters/fight_monster.html', context) if character.health > 0 else redirect(
            "character_has_died")
