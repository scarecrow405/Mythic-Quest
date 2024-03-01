from django.contrib import admin

from profiles.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'username', 'email', 'about', 'profile_image')
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')
