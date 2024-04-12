from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('admin/', admin.site.urls),

                  # Home Page
                  path("", include("home.urls")),

                  # Profiles
                  path("profile/", include("profiles.urls")),

                  # Characters
                  path("character/", include("characters.urls")),

                  # Monsters
                  path("monster/", include("monsters.urls")),

                  # Tavern
                  path("tavern/", include("tavern.urls")),

                  # Items
                  path("items/", include("items.urls")),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)

handler404 = 'characters.error_handling.handle_404'
