from django.urls import path

from items.views import items_potions

urlpatterns = [
    path("postions/", items_potions, name="items_potions"),
]
