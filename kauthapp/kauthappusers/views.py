from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from registration.forms import RegistrationFormUniqueEmail
from registration.signals import user_registered
from requests_oauthlib import OAuth2Session
from core.settings import TOAuthConfig as OAUTHCONFIG
from .services import (
    kong_create_consumer,
    kong_consumer_apikey,
    keycloak_create_account,
)
from kauthappusersapi.models import ApiKey


def landing_page(request):
    return redirect("/accounts/register/")


def oauth_google(request):
    oauth = OAuth2Session(
        OAUTHCONFIG.google.client_id,
        redirect_uri=OAUTHCONFIG.hostname_strict + OAUTHCONFIG.callback_path,
        scope=OAUTHCONFIG.google.scopes,
    )
    authorization_url, state = oauth.authorization_url(
        OAUTHCONFIG.google.auth_uri,
        access_type="offline",
        prompt="select_account",
    )
    request.session["oauth_state"] = state
    request.session["redirect_uri"] = oauth.redirect_uri
    return redirect(authorization_url)


def oauth_callback(request):
    oauth = OAuth2Session(
        OAUTHCONFIG.google.client_id,
        redirect_uri=request.session["redirect_uri"],
        scope=OAUTHCONFIG.google.scopes,
    )

    oauth.fetch_token(
        OAUTHCONFIG.google.token_uri,
        client_secret=OAUTHCONFIG.google.client_secret,
        authorization_response=OAUTHCONFIG.hostname_strict
        + OAUTHCONFIG.callback_path
        + "?"
        + request.META["QUERY_STRING"],
    )
    request.session["OAUTH_P"] = oauth.get(
        "https://www.googleapis.com/oauth2/v1/userinfo"
    ).json()
    return redirect("/oauth2provision")


def oauth_provision_setup(request):
    if request.method == "GET":
        F = RegistrationFormUniqueEmail(
            {
                "email": request.session["OAUTH_P"]["email"],
                "username": request.session["OAUTH_P"]["email"],
            }
        )
        return render(
            request,
            "kauthappusers/provision.html",
            context={"form": F},
        )

    F = RegistrationFormUniqueEmail(request.POST)
    new_user = F.save()
    user_registered.send(
        sender=F.__class__,
        user=new_user,
        request=request,
    )
    return redirect("/profile")


@receiver(signal=user_registered)
def oauth_provision_complete(request, sender, user, **kwargs):
    apikey = kong_consumer_apikey()
    if apikey.status_code == 201:
        new_key = apikey.content.json()["key"]
        key = ApiKey.objects.create(key=new_key, user=user)
    if key.id:
        keycloak_create_account(user.email)


@login_required
def profile(request):
    T = ApiKey.objects.filter(user__email__exact=request.user.email).first()
    return render(
        request,
        "kauthappusers/profile.html",
        {"token": T.key, "dt": str(T.issued_at)},
    )


def facebook_oauth(request):
    ...
