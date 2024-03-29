from django.urls import path

from characters.views import CharacterCreateView, CharacterDetailsView, CharacterEditView, CharacterDeleteView, \
    CharacterFightView, character_has_died, \
    handle_404, handle_403, CharacterDetailsPublicView

urlpatterns = [
    # Your Character CRUD
    path("create/", CharacterCreateView.as_view(), name="create_character"),
    path('details/<int:pk>/', CharacterDetailsView.as_view(), name='details_character'),
    path('edit/<int:pk>/', CharacterEditView.as_view(), name='edit_character'),
    path('delete/<int:pk>/', CharacterDeleteView.as_view(), name='delete_character'),

    # Public Character Read only
    path('public/details/<int:pk>/', CharacterDetailsPublicView.as_view(), name='public_details_character'),

    # Fight Character
    path('fight/<int:pk>/vs/<int:pk2>/', CharacterFightView.as_view(), name='fight_character'),
    path("death-screen/", character_has_died, name="character_has_died"),

    # Errors
    path('error/404/', handle_404, name='error_404'),
    path('error/403/', handle_403, name='error_403'),
]
