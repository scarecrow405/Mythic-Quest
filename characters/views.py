from math import ceil

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, UpdateView, DeleteView, TemplateView

from characters.forms import CharacterCreationForm, CharacterEditForm
from characters.models import Character

import random


@login_required
def create_character(request):
    has_character = Character.objects.filter(user=request.user).exists()
    if has_character:
        return redirect('details_character', pk=Character.objects.get(user=request.user).pk)

    if request.method == 'POST':
        form = CharacterCreationForm(request.POST)
        if form.is_valid():
            character = form.save(commit=False)
            character.user = request.user
            character.image_path = f'img/{request.POST.get("character_type", "")}-warrior.jpg'

            if "male" in character.image_path or "female" in character.image_path:
                character.save()
            else:
                messages.success(request, "Please select a character type!")
                return render(request, 'characters/create_character.html', {'form': form})

        return redirect('index')

    else:
        form = CharacterCreationForm()

    context = {
        'form': form,
    }

    return render(
        request,
        'characters/create_character.html',
        context
    )


class CharacterDetailsView(LoginRequiredMixin, DetailView):
    model = Character
    template_name = 'characters/details_character.html'
    context_object_name = 'character'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        character = self.get_object()
        is_user_gm = self.request.user.groups.filter(name='Game Master').exists() or self.request.user.is_superuser
        is_user_in_own_profile = self.request.user == character.user

        # Adds K if gold is greater than 10 000
        def get_character_stat(character_stat):
            if 9_999 >= character_stat >= 1_000:
                return f"{str(character_stat)[0]}.{str(character_stat)[1]}K"
            elif 99_999 >= character_stat >= 10_000:
                return f"{str(character_stat)[:2]}K"
            elif 999_999 >= character_stat >= 100_000:
                return f"{str(character_stat)[:3]}K"
            elif 99_999_999 >= character_stat >= 1_000_000:
                return f"{str(character_stat)[0]}.{str(character_stat)[1]}M"
            return character_stat

        # Add hero stats to the context
        context['character_stats'] = {
            'level': get_character_stat(character.level),
            'experience': get_character_stat(character.experience),
            'max_health': get_character_stat(character.max_health),
            'health': get_character_stat(character.health),
            'strength': get_character_stat(character.strength),
            'agility': get_character_stat(character.agility),
            'damage': get_character_stat(character.damage),
            'armor': get_character_stat(character.armor),
            'gold': get_character_stat(character.gold)
        }

        context["character_rating"] = character.rating
        context["is_user_gm"] = is_user_gm
        context["is_user_in_own_profile"] = is_user_in_own_profile

        return context


class CharacterEditView(LoginRequiredMixin, UpdateView):
    model = Character
    form_class = CharacterEditForm
    template_name = 'characters/edit_character.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owner = self.get_object().user

        context['owner'] = owner
        return context

    def get_success_url(self):
        return reverse('details_character', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        if self.request.method == 'POST':
            character = form.save(commit=False)

            # Character = plamenchoto's character
            # character.user = plamenchoto
            # self.request.user = plamenatron
            # character.user = self.request.user

            character_type = self.request.POST.get("character_type", "")

            if not character_type:
                form.add_error(None, "Please select a character type!")
                # messages.success(self.request, "Please select a character type!")
                return super().render_to_response(self.get_context_data(form=form))

            character.image_path = character_type
            character.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class CharacterDeleteView(LoginRequiredMixin, DeleteView):
    model = Character
    template_name = 'characters/delete_character.html'
    success_url = reverse_lazy('create_character')


def get_character_level(character_experience):
    level_thresholds = {
        1: 100,
        2: 200,
        3: 400,
        4: 800,
        5: 1600,
        6: 2500,
        7: 4000,
        8: 6400,
        9: 8100,
        10: 10000,
    }
    level = 1

    for lvl, threshold in level_thresholds.items():
        if character_experience >= threshold:
            level = lvl
    return level


def all_stats_increase(character) -> None:
    base_increase = {
        "max_health": 25,
        "health": 25,
        "strength": 12,
        "agility": 7,
        "damage": 10,
        "armor": 5
    }

    character.max_health += base_increase.get("max_health") * character.level
    character.health += base_increase.get("health") * character.level
    character.strength += base_increase.get("strength") * character.level
    character.agility += base_increase.get("agility") * character.level
    character.damage += base_increase.get("damage") * character.level
    character.armor += base_increase.get("armor") * character.level


def fight_experience_gain(player_level, opponent_level):
    base_experience_gain = {
        1: (10, 30),
        2: (20, 40),
        3: (30, 50),
        4: (40, 60),
        5: (50, 70),
        6: (60, 90),
        7: (70, 100),
        8: (80, 110),
        9: (90, 120),
        10: (100, 130),
    }

    base_range = base_experience_gain.get(player_level)

    level_difference = abs(player_level - opponent_level)
    modifier = max(0, 1 - (level_difference / 10))

    min_experience_gain = int(base_range[0] * modifier)
    max_experience_gain = int(base_range[1] * modifier)

    experience_gain = random.randint(min_experience_gain, max_experience_gain)
    return experience_gain


def gold_gained(player_level):
    base_gold_gain = {
        1: (50, 300),
        2: (80, 400),
        3: (111, 500),
        4: (140, 600),
        5: (210, 700),
        6: (290, 900),
        7: (420, 1000),
        8: (509, 1100),
        9: (630, 1200),
        10: (780, 1300),
    }

    base_range = base_gold_gain.get(player_level)

    min_experience_gain = int(base_range[0])
    max_experience_gain = int(base_range[1])

    gold_gain = random.randint(min_experience_gain, max_experience_gain)
    return gold_gain


class CharacterFightView(LoginRequiredMixin, View):

    def get(self, request, pk, pk2):
        try:
            character = Character.objects.get(pk=pk)
            enemy = Character.objects.get(pk=pk2)

        except Character.DoesNotExist:
            return render(request, 'home/index.html', {})

        # Return character to Tavern to heal.
        if character.health == 0:
            return redirect("character_has_died")

        if character.rating > enemy.rating:
            winner = character
        elif character.rating < enemy.rating:
            level_multiplier = abs(character.level - enemy.level)
            winner = character if random.randint(0, 100 * level_multiplier) == 0 else enemy
        else:
            winner = character if random.randint(0, 1) == 0 else enemy

        gained_exp = 0
        gained_gold = 0
        stolen_gold = 0

        if winner == character:
            # Enemy DMG & Your DMG
            enemy_damage = enemy.damage / 2
            your_damage = character.damage

            # Fight
            character.health = max(0, character.health - enemy_damage)
            if character.health > 0:
                enemy.health = max(0, enemy.health - your_damage)

                # Gain EXP
                gained_exp = fight_experience_gain(character.level, enemy.level)
                character.experience += gained_exp

                # Gain LVL
                current_level = character.level
                character.level = get_character_level(character.experience)

                # Increase all stats if lvl up!
                if current_level != character.level:
                    all_stats_increase(character)

                # Gold Stolen
                if character.level >= enemy.level:
                    stolen_gold_multiplier = max(1, abs(character.level - enemy.level)) / 50
                else:
                    stolen_gold_multiplier = abs(character.level - enemy.level) / (enemy.level / 2) / 50

                stolen_gold_percentage = 1 - stolen_gold_multiplier
                stolen_gold = ceil(enemy.gold * stolen_gold_multiplier)

                character.gold = ceil(character.gold + stolen_gold)
                enemy.gold = ceil(enemy.gold * stolen_gold_percentage)

                # Gain Gold
                gained_gold = gold_gained(character.level)
                character.gold += gained_gold
        else:
            enemy_damage = enemy.damage * 1.3
            your_damage = character.damage / 2
            # Fight
            character.health = max(0, character.health - enemy_damage)
            if character.health > 0:
                enemy.health = max(0, enemy.health - your_damage)

            # Save into DB
            character.save()
            enemy.save()

        context = {
            'character': character,
            'enemy': enemy,
            'winner': character if winner == character else enemy,
            'gained_gold': gained_gold,
            'gained_exp': gained_exp,
            'stolen_gold': stolen_gold,
        }

        return render(request, 'characters/character_fight.html', context)


def character_has_died(request):
    return render(request, 'characters/character-has-died.html', {})
