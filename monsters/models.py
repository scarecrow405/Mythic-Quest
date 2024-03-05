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

    image_path = models.CharField(
        max_length=MAX_IMAGE_PATH_LENGTH,
        null=True,
        blank=True)

    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.name
