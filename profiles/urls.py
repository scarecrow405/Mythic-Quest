from django.urls import path

from profiles.views import signup_user, signin_user, signout_user, user_profile_edit, user_profile_delete, \
    confirm_profile_delete

urlpatterns = [
    path('signup/', signup_user, name='signup'),
    path('signin/', signin_user, name='signin'),
    path("signout/", signout_user, name="signout"),

    path('edit/', user_profile_edit, name='profile_edit'),
    path('delete/', user_profile_delete, name='profile_delete'),
    path('confirm-delete/', confirm_profile_delete, name='confirm_profile_delete'),
]
