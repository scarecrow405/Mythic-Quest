from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from characters.models import Character


class HomeViewWithCharacter(LoginRequiredMixin, TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        try:
            character = Character.objects.get(user=user)
            character_stats = {
                'Level': character.level,
                'Experience': character.experience,
                'Health': character.health,
                'Strength': character.strength,
                'Agility': character.agility,
                'Damage': character.damage,
                'Armor': character.armor,
                'Gold': character.gold,
            }

            enemy_characters = Character.objects.exclude(user=user).order_by('-rating')

            context['character'] = character
            context['character_stats'] = character_stats
            context['character_rating'] = character.rating
            context['enemy_characters'] = enemy_characters

        except Character.DoesNotExist:
            all_characters = Character.objects.order_by('-rating')
            context['all_characters'] = all_characters
        return context


class HomeViewWithoutCharacter(TemplateView):
    template_name = 'home/index-without-character.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_characters = Character.objects.order_by('-rating')
        context['all_characters'] = all_characters

        return context


class ContactViewForm(LoginRequiredMixin, TemplateView):
    template_name = 'home/contact-form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_email'] = user.email
        return context
