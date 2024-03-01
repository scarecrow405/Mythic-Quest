from django.contrib.auth.models import User
from django.db import models

STARTING_LEVEL = 1
STARTING_EXPERIENCE = 0
STARTING_HEALTH = 100
STARTING_STRENGTH = 5
STARTING_AGILITY = 5
STARTING_DAMAGE = 10
STARTING_ARMOR = 5
STARTING_GOLD = 0
STARTING_RATING = 0


class Character(models.Model):
    MAX_NICKNAME_LENGTH = 10
    MAX_IMAGE_PATH_LENGTH = 400

    user = models.OneToOneField(
        to=User,
        null=True,
        on_delete=models.CASCADE,
    )

    nickname = models.CharField(
        max_length=MAX_NICKNAME_LENGTH,
        null=False,
        blank=False,
    )

    image_path = models.CharField(
        max_length=MAX_IMAGE_PATH_LENGTH,
        null=False,
        blank=False,
    )

    # Character Stats
    level = models.IntegerField(default=STARTING_LEVEL)
    experience = models.IntegerField(default=STARTING_EXPERIENCE)
    health = models.IntegerField(default=STARTING_HEALTH)
    strength = models.IntegerField(default=STARTING_STRENGTH)
    agility = models.IntegerField(default=STARTING_AGILITY)
    damage = models.IntegerField(default=STARTING_DAMAGE)
    armor = models.IntegerField(default=STARTING_ARMOR)
    gold = models.IntegerField(default=STARTING_GOLD)
    rating = models.FloatField(default=STARTING_RATING)

    def calculate_rating(self, **character_stats):
        weights = {
            'Level': 1.5,
            'Experience': 1.7,
            'Health': 1.1,
            'Strength': 1.8,
            'Agility': 1.5,
            'Damage': 1.5,
            'Armor': 1.2,
        }

        current_rating = 0
        for name, amount in character_stats.items():
            if name in weights:
                current_rating += weights[name] * amount
        self.rating = current_rating

    def save(self, *args, **kwargs):
        character_stats = {
            'Level': self.level,
            'Health': self.health,
            'Strength': self.strength,
            'Agility': self.agility,
            'Damage': self.damage,
            'Armor': self.armor,
        }

        self.calculate_rating(**character_stats)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nickname
