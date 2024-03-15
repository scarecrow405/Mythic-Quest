from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from items.models import Item


class PotionShopView(TemplateView):
    template_name = 'items/potions.html'
    queryset = Item.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_items'] = Item.objects.order_by("id")
        return context

    def experience_potion(self, character, potion):
        exp_boost = apply_experience_potion(character, potion)
        character.experience += exp_boost
        character.save()

    def post(self, request, *args, **kwargs):
        character = request.user.character

        if 'buy_item' in request.POST:
            item_id = request.POST.get('item_id')
            item = Item.objects.get(pk=item_id)

            if item.effect == 'EXP Boost':
                if check_player_has_enough_gold(character, item):
                    character.gold -= item.price
                    self.experience_potion(character, item)
                else:
                    messages.error(request, "You don't have enough gold!")
                    return redirect("items_potions")

        return redirect('details_character', pk=character.pk)


def check_player_has_enough_gold(character, potion):
    return character.gold >= potion.price


def apply_experience_potion(character, potion):
    exp_threshold = get_next_level_experience_threshold(character)
    exp_boost = exp_threshold * potion.boost_amount_percentage / 100
    return exp_boost


def get_next_level_experience_threshold(character):
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

    current_max_level = 10
    exp_threshold = level_thresholds.get(min(character.level + 1, current_max_level))

    return exp_threshold
