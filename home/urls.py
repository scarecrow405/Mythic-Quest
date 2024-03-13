from django.urls import path

from home.views import HomeViewWithCharacter, HomeViewWithoutCharacter, ContactViewForm

urlpatterns = [
    path('', HomeViewWithCharacter.as_view(), name='index'),
    path('public/', HomeViewWithoutCharacter.as_view(), name='index-without-character'),

    path('contact-form/', ContactViewForm.as_view(), name='contact-form'),
]
