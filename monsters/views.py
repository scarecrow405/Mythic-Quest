from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from monsters.models import Monster
from monsters.monster_fight_logic import monster_fight


class DungeonView(LoginRequiredMixin, TemplateView):
    template_name = 'monsters/dungeon.html'

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

        winner, gained_exp, gained_gold, stolen_gold, win_chance = monster_fight(character, monster)

        return render(request, self.template_name)


"""
class CharacterFightView(LoginRequiredMixin, View):

    def get(self, request, pk, pk2):
        try:
            character = Character.objects.get(pk=pk)
            enemy = Character.objects.get(pk=pk2)

            # Check if the user is viewing their own character
            is_own_character = character.user == request.user

            # Render index page based on whether the user has a character or not
            if is_own_character:
                index_template = 'home/index.html'
            else:
                index_template = 'home/index-without-character.html'

        except Character.DoesNotExist:
            # Render a custom error page if characters are not found
            return redirect('error_404')

        # Return character to Tavern to heal.
        if character.health == 0:
            return redirect("character_has_died")

        # Resolve Fight
        winner, gained_exp, gained_gold, stolen_gold, win_chance = resolve_fight(character, enemy)

        context = {
            'character': character,
            'enemy': enemy,
            'winner': winner,
            'gained_gold': gained_gold,
            'gained_exp': gained_exp,
            'stolen_gold': stolen_gold,
            'win_chance': win_chance
        }

        return render(request, 'characters/character_fight.html', context) if character.health > 0 else redirect(
            "character_has_died")
            """
