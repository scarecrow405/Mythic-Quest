from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from profiles.models import UserProfile


class SignupForm(forms.ModelForm):
    MIN_PASSWORD_LENGTH = 8

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'placeholder': 'Password', 'id': 'pass1'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password', 'id': 'pass2'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'id': 'username'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email', 'id': 'email'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for (e, field) in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = True
            self.fields[e].help_text = None

    def clean_username(self):
        username = self.cleaned_data['username']
        min_username_length = UserProfile.MIN_USERNAME_LENGTH
        max_username_length = UserProfile.MAX_USERNAME_LENGTH

        if len(username) < min_username_length:
            raise forms.ValidationError(f'Username must be at least {min_username_length} characters long.')
        elif len(username) > max_username_length:
            raise forms.ValidationError(f'Username must be at most {max_username_length} characters long.')
        return username

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if len(password1) < self.MIN_PASSWORD_LENGTH:
            raise forms.ValidationError(f'Password must be at least {self.MIN_PASSWORD_LENGTH} characters long.')
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')
        return password2


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['about', 'profile_image', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for (e, field) in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control mb-3'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control mb-3'}))


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'about', 'profile_image']
