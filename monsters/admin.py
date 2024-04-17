from django.contrib import admin
from monsters.models import Monster


def get_description(description):
    return description[:40]


@admin.register(Monster)
class MonsterAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "level",
        "health",
        "strength",
        "agility",
        "damage",
        "armor",
        "base_gold_gained",
        "base_exp_gained",
        "image_path",
        "rating",
    )

    list_filter = ("level", "name")
    ordering = ("level",)
