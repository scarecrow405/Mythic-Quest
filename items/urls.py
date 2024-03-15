from django.urls import path

from items.views import PotionShopView

# from items.views import items_potions

urlpatterns = [
    path("postions/", PotionShopView.as_view(), name="items_potions"),
]
