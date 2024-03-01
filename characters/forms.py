from django import forms
from .models import Character


class CharacterCreationForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ["nickname"]


class CharacterEditForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ["nickname"]
