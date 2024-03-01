from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    MAX_USERNAME_LENGTH = 30
    MIN_USERNAME_LENGTH = 2

    ABOUT_MAX_LENGTH = 300
    ABOUT_MIN_LENGTH = 10

    user = models.OneToOneField(
        to=User,
        null=True,
        on_delete=models.CASCADE, )

    username = models.CharField(
        max_length=MAX_USERNAME_LENGTH,
        validators=[MinLengthValidator(MIN_USERNAME_LENGTH)],
        null=False,
        blank=False,
        unique=True,
    )

    email = models.EmailField(
        null=False,
        blank=False,
    )

    about = models.TextField(
        max_length=ABOUT_MAX_LENGTH,
        validators=[MinLengthValidator(ABOUT_MIN_LENGTH)],
        null=True,
        blank=True, )

    profile_image = models.ImageField(
        upload_to='profile_images/',
        null=True,
        blank=True, )

    def __str__(self):
        return self.user.username
