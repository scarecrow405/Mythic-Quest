from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, ListView

from characters.models import Character


class HomeViewWithCharacter(LoginRequiredMixin, ListView):
    queryset = Character.objects.order_by('-rating')
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        search_query = self.request.GET.get('character_nickname', '').strip()

        page = self.request.GET.get('page', 1)

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

            enemy_characters = Character.objects.exclude(user=user).filter(nickname__icontains=search_query).order_by(
                '-rating')

            paginated_characters = Paginator(enemy_characters, 3)
            if int(page) > paginated_characters.num_pages:
                page = 1

            paginated_enemy_characters = paginated_characters.page(page)

            context['character'] = character
            context['character_stats'] = character_stats
            context['character_rating'] = character.rating
            context['enemy_characters'] = paginated_enemy_characters

            context['paginator_object'] = paginated_characters
            context['page'] = page

        except Character.DoesNotExist:
            all_characters = Character.objects.order_by('-rating')
            context['all_characters'] = all_characters
        return context


# class HomeViewWithoutCharacter(TemplateView):
#     template_name = 'home/index-without-character.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         all_characters = Character.objects.order_by('-rating')
#         context['all_characters'] = all_characters
#
#         return context

class HomeViewWithoutCharacter(ListView):
    queryset = Character.objects.order_by('-rating')
    template_name = 'home/index-without-character.html'
    paginate_by = 10

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context['character_nickname_pattern'] = self.request.GET.get('character_nickname', '').strip()
    #     return context
    #
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return self.search_by_character_nickname(queryset)
    #
    # def search_by_character_nickname(self, queryset):
    #     character_nickname_pattern = self.request.GET.get('character_nickname', '').strip()
    #     if character_nickname_pattern:
    #         return queryset.filter(nickname__icontains=character_nickname_pattern)
    #     return queryset


class ContactViewForm(LoginRequiredMixin, TemplateView):
    template_name = 'home/contact-form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_email'] = user.email
        return context
