from django.urls import path

from tavern.views import tavern, heal_for_10_percent

urlpatterns = [
    path('', tavern, name='tavern'),
    path('heal-10/', heal_for_10_percent, name='heal_for_10_percent'),
]
