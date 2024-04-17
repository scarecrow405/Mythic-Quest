from django.core import validators
from django.db import models

GAME_NAME_MAX_LEN = 100
GAME_DESCRIPTION_MAX_LEN = 250


class Game(models.Model):
    name = models.CharField(
        max_length=GAME_NAME_MAX_LEN,
        unique=True,
        blank=False,
        null=False,

    )

    description = models.TextField(
        max_length=GAME_DESCRIPTION_MAX_LEN,
        null=True,
        blank=True,
    )

    number_of_clicks_required = models.IntegerField(
        default=0,
        validators=[
            validators.MinValueValidator(0),
        ],
    )

    gold_to_gain = models.IntegerField(default=0)
