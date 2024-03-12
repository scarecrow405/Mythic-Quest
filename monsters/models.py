from django.db import models

MAX_NAME_LENGTH = 32
MAX_IMAGE_PATH_LENGTH = 255


class Monster(models.Model):
    name = models.CharField(max_length=MAX_NAME_LENGTH)
    description = models.TextField()

    level = models.IntegerField()
    health = models.IntegerField()
    strength = models.IntegerField()
    agility = models.IntegerField()
    damage = models.IntegerField()
    armor = models.IntegerField()

    base_gold_gained = models.IntegerField()
    base_exp_gained = models.IntegerField()

    image_path = models.CharField(
        max_length=MAX_IMAGE_PATH_LENGTH,
        null=True,
        blank=True)

    rating = models.IntegerField(default=0)

    def calculate_rating(self, **character_stats):
        weights = {
            'Level': 2,
            'Health': 1.5,
            'Strength': 2,
            'Agility': 1.6,
            'Damage': 1.6,
            'Armor': 1.301,
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
        return self.name
