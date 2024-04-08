from django.core.management.base import BaseCommand
from items.models import Item


class Command(BaseCommand):
    help = 'Seed the database with initial items'

    def handle(self, *args, **options):
        items = [
            {
                'name': 'Experience Potion',
                'description': 'Instantly gain 10% experience based on your current max level.',
                'effect': 'EXP Boost',
                'boost_amount_percentage': 10,
                'image_path': 'img/potions/experience-potion.png',
                'price': 5000
            },

            {
                'name': 'Health Potion',
                'description': 'Permanently increase max health by 10%.',
                'effect': 'Max Health Boost',
                'boost_amount_percentage': 10,
                'image_path': 'img/potions/health-potion.png',
                'price': 5000
            },

            {
                'name': 'Strength Potion',
                'description': 'Permanently increase strength by 10%.',
                'effect': 'Strength Boost',
                'boost_amount_percentage': 10,
                'image_path': 'img/potions/strength-potion.png',
                'price': 5000
            },

            {
                'name': 'Agility Potion',
                'description': 'Permanently increase agility by 10%.',
                'effect': 'Agility Boost',
                'boost_amount_percentage': 10,
                'image_path': 'img/potions/agility-potion.png',
                'price': 5000
            },

            {
                'name': 'Damage Potion',
                'description': 'Permanently increase damage by 10%.',
                'effect': 'Damage Boost',
                'boost_amount_percentage': 10,
                'image_path': 'img/potions/damage-potion.png',
                'price': 5000
            },

            {
                'name': 'Armor Potion',
                'description': 'Permanently increase armor by 10%.',
                'effect': 'Armor Boost',
                'boost_amount_percentage': 10,
                'image_path': 'img/potions/armor-potion.png',
                'price': 5000
            },

            {
                'name': 'Ultra Potion',
                'description': 'Permanently increase all stats by 2%.',
                'effect': 'All Stats Boost',
                'boost_amount_percentage': 2,
                'image_path': 'img/potions/ultra-potion.png',
                'price': 9999
            },

        ]

        for item_data in items:
            Item.objects.create(**item_data)

        self.stdout.write(self.style.SUCCESS('Items seeded successfully!'))
