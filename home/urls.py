from django.urls import path

from home.views import HomeViewWithCharacter, HomeViewWithoutCharacter

urlpatterns = [
    path('', HomeViewWithCharacter.as_view(), name='index'),
    path('', HomeViewWithoutCharacter.as_view(), name='index-without-character'),
]
