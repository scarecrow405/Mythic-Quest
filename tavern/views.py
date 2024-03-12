from math import ceil

from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse


def tavern(request):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        character = request.user.character
        character_level = character.level
        character_gold = character.gold

        gold_costs = {
            'heal_10_percent': calculate_gold_cost(character_level, 10),
            'heal_50_percent': calculate_gold_cost(character_level, 50),
            'heal_100_percent': calculate_gold_cost(character_level, 100)
        }

        can_afford_heal_10_percent = check_character_has_enough_gold(character_gold,
                                                                     gold_costs['heal_10_percent'])
        can_afford_heal_50_percent = check_character_has_enough_gold(character_gold,
                                                                     gold_costs['heal_50_percent'])
        can_afford_heal_100_percent = check_character_has_enough_gold(character_gold,
                                                                      gold_costs['heal_100_percent'])

        context = {
            'gold_costs': gold_costs,
            'can_afford_heal_10_percent': can_afford_heal_10_percent,
            'can_afford_heal_50_percent': can_afford_heal_50_percent,
            'can_afford_heal_100_percent': can_afford_heal_100_percent
        }

        return render(request, "tavern/tavern.html", context)


def calculate_gold_cost(character_level, percent_to_heal):
    base_gold_cost = 10
    if percent_to_heal == 50:
        base_gold_cost = 50
    elif percent_to_heal == 100:
        base_gold_cost = 100

    scaling_factor = 4 + (character_level / 10)

    gold_cost = base_gold_cost * scaling_factor
    gold_cost = round(gold_cost)

    return gold_cost


def check_character_has_enough_gold(character_gold, gold_cost):
    return character_gold >= gold_cost


def check_for_errors(request, character, gold_cost, character_max_hp):
    if not check_character_has_enough_gold(character.gold, gold_cost):
        messages.error(request, "You don't have enough gold to heal.")
        return True
    if character.health == character_max_hp:
        messages.error(request, "You are already at full health.")
        return True


def heal_for_10_percent(request):
    if request.method == 'POST':
        character = request.user.character
        character_max_hp = character.max_health
        character_level = character.level

        amount_to_heal = int(character_max_hp * 0.1)
        gold_cost = calculate_gold_cost(character_level, 10)

        # Validate That character has enough gold and isn't full HP
        if check_for_errors(request, character, gold_cost, character_max_hp):
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

        # Validate That character has enough gold and isn't full HP
        if check_for_errors(request, character, gold_cost, character_max_hp):
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

        # Validate That character has enough gold and isn't full HP
        if check_for_errors(request, character, gold_cost, character_max_hp):
            return redirect('tavern')

        character.gold -= gold_cost
        character.health = character_max_hp
        character.save()

        return redirect(reverse('details_character', kwargs={'pk': character.pk}))
    else:
        return redirect('index')
