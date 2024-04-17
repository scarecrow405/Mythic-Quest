from django.contrib import admin

from games.models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'number_of_clicks_required', 'gold_to_gain')
    list_filter = ('name', 'description', 'number_of_clicks_required', 'gold_to_gain')
    search_fields = ('name', 'description', 'number_of_clicks_required', 'gold_to_gain')
