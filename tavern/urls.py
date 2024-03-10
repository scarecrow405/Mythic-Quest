from django.urls import path

from tavern.views import tavern, heal_for_10_percent, heal_for_50_percent, heal_for_100_percent

urlpatterns = [
    path('', tavern, name='tavern'),
    path('heal-10/', heal_for_10_percent, name='heal_for_10_percent'),
    path('heal-50/', heal_for_50_percent, name='heal_for_50_percent'),
    path('heal-100/', heal_for_100_percent, name='heal_for_100_percent'),
]
