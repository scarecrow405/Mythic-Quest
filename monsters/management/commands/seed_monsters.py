import random

from django.core.management.base import BaseCommand

from monsters.models import Monster


class Command(BaseCommand):
    help = 'Seed the database with initial monsters'

    def handle(self, *args, **options):
        monsters = [
            {
                'name': 'Scarab Beetle',
                'description': 'A giant beetle with formidable strength and armor.',
                'level': 1,
                'health': 80,
                'strength': 5,
                'agility': 5,
                'damage': 5,
                'armor': 5,
                'rating': 0,
                'image_path': 'img/scarab-beetle-monster.png',
                'base_gold_gained': 100,
                'base_exp_gained': 20,
            },
            {
                'name': 'Evil Mummy',
                'description': 'An undead mummy risen from its tomb, seeking vengeance.',
                'level': 10,
                'health': 180,
                'strength': 25,
                'agility': 15,
                'damage': 30,
                'armor': 25,
                'rating': 0,
                'image_path': 'img/evil-mummy-monster.png',
                'base_gold_gained': 2000,
                'base_exp_gained': 300,
            },
            {
                'name': 'Anubis',
                'description': 'A powerful deity of ancient Egypt, guarding the secrets of the underworld.',
                'level': 35,
                'health': 500,
                'strength': 70,
                'agility': 65,
                'damage': 90,
                'armor': 100,
                'rating': 0,
                'image_path': 'img/anubis-monster.png',
                'base_gold_gained': 14000,
                'base_exp_gained': 5000,
            },
            {
                'name': 'Judge the Destroyer',
                'description': 'The fearsome Judge the Destroyer, ruler of the digital realm! With lightning eyes and a thunderous gavel, this ultimate foe challenges all who dare to test their code against its scrutiny.',
                'level': 9999,
                'health': 9999,
                'strength': 9999,
                'agility': 9999,
                'damage': 9999,
                'armor': 9999,
                'rating': 0,
                'image_path': 'img/judge-the-destroyer2-monster.jpg',
                'base_gold_gained': 999999999,
                'base_exp_gained': 99999,
            },
        ]

        for monster_data in monsters:
            Monster.objects.create(**monster_data)

        self.stdout.write(self.style.SUCCESS('Monsters seeded successfully!'))
