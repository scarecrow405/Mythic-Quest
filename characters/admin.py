from django.contrib import admin

from characters.models import Character


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = (
        'nickname',
        'level',
        'max_health',
        'health',
        'strength',
        'agility',
        'damage',
        'armor',
    )
