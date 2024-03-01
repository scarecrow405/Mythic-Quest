from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home Page
    path("", include("home.urls")),

    # Profiles
    path("profile/", include("profiles.urls")),

    # Characters
    path("character/", include("characters.urls"))
]
