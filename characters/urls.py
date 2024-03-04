from django.urls import path

from characters.views import create_character, CharacterDetailsView, CharacterEditView, CharacterDeleteView, \
    CharacterFightView

urlpatterns = [
    # Your Character
    path("create/", create_character, name="create_character"),
    path('details/<int:pk>/', CharacterDetailsView.as_view(), name='details_character'),
    path('edit/<int:pk>/', CharacterEditView.as_view(), name='edit_character'),
    path('delete/<int:pk>/', CharacterDeleteView.as_view(), name='delete_character'),

    # Fight Character
    path('fight/<int:pk>/vs/<int:pk2>/', CharacterFightView.as_view(), name='fight_character'),

    # Enemy Character
    # path('details/<int:pk>/enemy/', EnemyCharacterDetailsView.as_view(), name='details_enemy_character'),
]
