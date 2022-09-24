from django.urls import path
from . import views


urlpatterns = [
    path("google", views.oauth_google, name="oauth_google"),
    path("oauth2callback", views.oauth_callback, name="oauth_google_callback"),
    path("facebook", views.facebook_oauth, name="facebook_oauth"),
    path("oauth2provision", views.oauth_provision_setup, name="provision_user_account"),
    path("profile", views.profile, name="profile"),
    path("", views.landing_page, name="landing"),
]
