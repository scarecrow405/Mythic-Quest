from django.db import models

MAX_ITEM_NAME_LENGTH = 35
MAX_EFFECT_LENGTH = 100

ITEM_CHOICES = (
    ("EXP Boost", "EXP Boost"),
    ("Max Health Boost", "Max Health Boost"),
    ("Strength Boost", "Strength Boost"),
    ("Agility Boost", "Agility Boost"),
    ("Damage Boost", "Damage Boost"),
    ("Armor Boost", "Armor Boost"),

    # the most expensive one
    ("All Stats Boost", "All Stats Boost"),
)


class Item(models.Model):
    name = models.CharField(
        max_length=MAX_ITEM_NAME_LENGTH,
        unique=True,
        blank=False,
        null=False,
    )

    description = models.TextField(blank=True, null=True)

    effect = models.CharField(
        max_length=MAX_EFFECT_LENGTH,
        choices=ITEM_CHOICES,
        blank=False,
        null=False,
    )

    boost_amount_percentage = models.IntegerField(default=0)

    image_path = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
