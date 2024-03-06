from math import ceil

from django.shortcuts import render, redirect
from django.urls import reverse


def tavern(request):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        pass

    return render(request, "tavern/tavern.html")


def heal_for_10_percent(request):
    if request.method == 'POST':
        character = request.user.character
        character_max_hp = character.max_health

        amount_to_heal = int(character_max_hp * 0.1)
        new_health = min(character.health + amount_to_heal, character_max_hp)

        character.health = new_health
        character.save()

        return redirect(reverse('details_character', kwargs={'pk': character.pk}))
    else:
        return redirect('index')
