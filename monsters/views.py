from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

from monsters.models import Monster


class DungeonView(LoginRequiredMixin, TemplateView):
    template_name = 'monsters/dungeon.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['monsters'] = Monster.objects.order_by('rating')
        return context


class MonsterFightView(LoginRequiredMixin, TemplateView):
    template_name = 'monsters/fight_monster.html'
