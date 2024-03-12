from math import ceil

from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse


def tavern(request):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        pass

    return render(request, "tavern/tavern.html")


def calculate_gold_cost(character_level, percent_to_heal):
    # TODO: Add formula for gold cost!
    gold_cost = 0
    if percent_to_heal == 10:
        gold_cost = 10
    elif percent_to_heal == 50:
        gold_cost = 50
    elif percent_to_heal == 100:
        gold_cost = 100
    return gold_cost


def check_character_has_enough_gold(request, character_gold, gold_cost):
    return character_gold >= gold_cost


def heal_for_10_percent(request):
    if request.method == 'POST':
        character = request.user.character
        character_max_hp = character.max_health
        character_level = character.level

        amount_to_heal = int(character_max_hp * 0.1)
        gold_cost = calculate_gold_cost(character_level, 10)

        if not check_character_has_enough_gold(request, character.gold, gold_cost):
            messages.error(request, "You don't have enough gold to heal.")
            return redirect('tavern')

        new_health = min(character.health + amount_to_heal, character_max_hp)

        character.gold -= gold_cost
        character.health = new_health
        character.save()

        return redirect(reverse('details_character', kwargs={'pk': character.pk}))
    else:
        return redirect('index')


def heal_for_50_percent(request):
    if request.method == 'POST':
        character = request.user.character
        character_max_hp = character.max_health
        character_level = character.level

        amount_to_heal = int(character_max_hp * 0.5)
        gold_cost = calculate_gold_cost(character_level, 50)

        if not check_character_has_enough_gold(request, character.gold, gold_cost):
            messages.error(request, "You don't have enough gold to heal.")
            return redirect('tavern')

        new_health = min(character.health + amount_to_heal, character_max_hp)

        character.gold -= gold_cost
        character.health = new_health
        character.save()

        return redirect(reverse('details_character', kwargs={'pk': character.pk}))
    else:
        return redirect('index')


def heal_for_100_percent(request):
    if request.method == 'POST':
        character = request.user.character
        character_max_hp = character.max_health
        character_level = character.level

        gold_cost = calculate_gold_cost(character_level, 100)

        if not check_character_has_enough_gold(request, character.gold, gold_cost):
            messages.error(request, "You don't have enough gold to heal.")
            return redirect('tavern')

        character.gold -= gold_cost
        character.health = character_max_hp
        character.save()

        return redirect(reverse('details_character', kwargs={'pk': character.pk}))
    else:
        return redirect('index')
