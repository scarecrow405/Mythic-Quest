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
            pass
        return context


class HomeViewWithoutCharacter(LoginRequiredMixin, TemplateView):
    pass
    # def get(self, request, pk, pk2):
    #     try:
    #         character = Character.objects.get(pk=pk)
    #         enemy = Character.objects.get(pk=pk2)
    #     except Character.DoesNotExist:
    #         return render(request, 'home/index.html')
    #
    #     winner = character
    #
    #     context = {
    #         'character1': character,
    #         'character2': enemy,
    #         'winner': winner,
    #     }


class ContactViewForm(TemplateView):
    template_name = 'home/contact-form.html'

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        print(request.body)
        if email != request.user.email:
            messages.error(request, "The email you entered does not match your logged-in email.")
            return redirect('contact_form')
