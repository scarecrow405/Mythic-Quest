from time import sleep

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from characters.fight_logic import all_stats_increase
from characters.get_character_level import get_character_level
from items.models import Item

from items.potions_effects import (
    apply_health_potion, apply_strength_potion, apply_agility_potion,
    apply_damage_potion, apply_experience_potion, apply_ultra_potion,
    apply_armor_potion
)


class PotionShopView(LoginRequiredMixin, TemplateView):
    template_name = 'items/potions.html'
    queryset = Item.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_items'] = Item.objects.order_by("id")
        return context

    def experience_potion(self, character, potion):
        exp_boost = apply_experience_potion(character, potion)
        character.experience += exp_boost

        # Gain LVL
        current_level = character.level
        character.level = get_character_level(character.experience)

        # Increase all stats if lvl up!
        if current_level != character.level:
            all_stats_increase(character)
        character.save()

    def health_potion(self, character, potion):
        health_boost = apply_health_potion(character, potion)
        character.max_health += health_boost
        character.save()

    def strength_potion(self, character, potion):
        strength_boost = apply_strength_potion(character, potion)
        character.strength += strength_boost
        character.save()

    def agility_potion(self, character, potion):
        agility_boost = apply_agility_potion(character, potion)
        character.agility += agility_boost
        character.save()

    def damage_potion(self, character, potion):
        damage_boost = apply_damage_potion(character, potion)
        character.damage += damage_boost
        character.save()

    def armor_potion(self, character, potion):
        armor_boost = apply_armor_potion(character, potion)
        character.armor += armor_boost
        character.save()

    def ultra_potion(self, character, potion):
        bonus_max_health, bonus_strength, bonus_agility, bonus_damage, bonus_armor = apply_ultra_potion(character,
                                                                                                        potion)
        character.max_health += bonus_max_health
        character.strength += bonus_strength
        character.agility += bonus_agility
        character.damage += bonus_damage
        character.armor += bonus_armor
        character.save()

    def post(self, request, *args, **kwargs):
        character = request.user.character

        if 'buy_item' in request.POST:
            item_id = request.POST.get('item_id')
            item = Item.objects.get(pk=item_id)

            not_enough_gold = False

            if item.effect == 'EXP Boost':
                if check_player_has_enough_gold(character, item):
                    character.gold -= item.price
                    self.experience_potion(character, item)
                else:
                    not_enough_gold = True

            elif item.effect == "Max Health Boost":
                if check_player_has_enough_gold(character, item):
                    character.gold -= item.price
                    self.health_potion(character, item)
                else:
                    not_enough_gold = True

            elif item.effect == "Strength Boost":
                if check_player_has_enough_gold(character, item):
                    character.gold -= item.price
                    self.strength_potion(character, item)
                else:
                    not_enough_gold = True

            elif item.effect == "Agility Boost":
                if check_player_has_enough_gold(character, item):
                    character.gold -= item.price
                    self.agility_potion(character, item)
                else:
                    not_enough_gold = True

            elif item.effect == "Damage Boost":
                if check_player_has_enough_gold(character, item):
                    character.gold -= item.price
                    self.damage_potion(character, item)
                else:
                    not_enough_gold = True

            elif item.effect == "Armor Boost":
                if check_player_has_enough_gold(character, item):
                    character.gold -= item.price
                    self.armor_potion(character, item)
                else:
                    not_enough_gold = True

            elif item.effect == "All Stats Boost":
                if check_player_has_enough_gold(character, item):
                    character.gold -= item.price
                    self.ultra_potion(character, item)
                else:
                    not_enough_gold = True

            if not_enough_gold:
                messages.error(request, "You don't have enough gold!")
                return redirect("items_potions")

        return redirect('details_character', pk=character.pk)


def check_player_has_enough_gold(character, potion):
    return character.gold >= potion.price
