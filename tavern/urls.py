from django.urls import path

from tavern.views import tavern

urlpatterns = [
    path('', tavern, name='tavern'),
]
