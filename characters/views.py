from math import ceil

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, UpdateView, DeleteView, TemplateView

from characters.fight_logic import resolve_fight
from characters.forms import CharacterCreationForm, CharacterEditForm
from characters.models import Character

import random

from characters.show_character_stats import get_character_stat
from characters.error_handling import handle_404, handle_403


# @login_required
# def create_character(request):
#     has_character = Character.objects.filter(user=request.user).exists()
#     if has_character:
#         return redirect('details_character', pk=Character.objects.get(user=request.user).pk)
#
#     if request.method == 'POST':
#         form = CharacterCreationForm(request.POST)
#         if form.is_valid():
#             character = form.save(commit=False)
#             character.user = request.user
#             character.image_path = f'img/{request.POST.get("character_type", "")}-warrior.jpg'
#
#             if "male" in character.image_path or "female" in character.image_path:
#                 character.save()
#             else:
#                 messages.success(request, "Please select a character type!")
#                 return render(request, 'characters/create_character.html', {'form': form})
#
#         return redirect('index')
#
#     else:
#         form = CharacterCreationForm()
#
#     context = {
#         'form': form,
#     }
#
#     return render(
#         request,
#         'characters/create_character.html',
#         context
#     )


class CharacterCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'characters/create_character.html'

    def get(self, request, *args, **kwargs):
        has_character = Character.objects.filter(user=request.user).exists()
        if has_character:
            return redirect('details_character', pk=Character.objects.get(user=request.user).pk)
        form = CharacterCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CharacterCreationForm(request.POST)
        if form.is_valid():
            character = form.save(commit=False)
            character.user = request.user
            character.image_path = f'img/{request.POST.get("character_type", "")}-warrior.jpg'
            if "male" in character.image_path or "female" in character.image_path:
                character.save()
                return redirect('index')
            else:
                messages.success(request, "Please select a character type!")
        return render(request, self.template_name, {'form': form})


class CharacterDetailsView(LoginRequiredMixin, DetailView):
    model = Character
    template_name = 'characters/details_character.html'
    context_object_name = 'character'

    # TODO: Sometimes it's not working or it's loading slow in my browser?
    def get(self, request, *args, **kwargs):
        try:
            character = Character.objects.get(pk=kwargs.get('pk'))
        except Character.DoesNotExist:
            return redirect('error_404')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        character = self.get_object()

        is_user_gm = self.request.user.groups.filter(name='Game Master').exists() or self.request.user.is_superuser
        is_user_in_own_profile = self.request.user == character.user

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

    def get(self, request, *args, **kwargs):
        try:
            character = Character.objects.get(pk=kwargs.get('pk'))
        except Character.DoesNotExist:
            return redirect('error_404')
        return super().get(request, *args, **kwargs)

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


def character_has_died(request):
    return render(request, 'characters/character-has-died.html', {})
