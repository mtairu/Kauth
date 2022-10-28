import secrets
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from core.settings import (
    TOAuthConfig as OAUTHCONFIG,
    DJ_K_API_BASEURI,
    DJ_KONG_ADMINAPI_BASEURI,
)
from django.contrib.auth.hashers import make_password
from kauthappusersapi.models import UserAccessToken, ClientAccessToken

from registration.forms import RegistrationFormUniqueEmail
from registration.signals import user_registered

from requests_oauthlib import OAuth2Session
import requests as rq


def landing_page(request):
    return redirect("/accounts/register/")


def oauth_google(request):
    oauth = OAuth2Session(
        OAUTHCONFIG.google.client_id,
        redirect_uri=OAUTHCONFIG.hostname_strict + OAUTHCONFIG.callback_path,
        scope=OAUTHCONFIG.google.scopes,
    )
    authorization_url, state = oauth.authorization_url(
        OAUTHCONFIG.google.auth_uri, access_type="offline", prompt="select_account"
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
    profile = oauth.get("https://www.googleapis.com/oauth2/v1/userinfo")
    request.session["OAUTH_P"] = profile.json()
    return redirect("/oauth2provision")


def oauth_provision_setup(request):
    if request.method == "GET":
        F = RegistrationFormUniqueEmail(
            {
                "email": request.session["OAUTH_P"]["email"],
                "username": request.session["OAUTH_P"]["email"],
            }
        )
        return render(request, "kauthappusers/provision.html", context={"form": F})

    F = RegistrationFormUniqueEmail(request.POST)
    new_user = F.save()
    user_registered.send(sender=F.__class__, user=new_user, request=request)
    return redirect("/profile")


def kong_apikey(email):
    resp = rq.post(f"{DJ_KONG_ADMINAPI_BASEURI}/consumers/", json={"username": email})
    if resp.status_code == 201:
        return rq.post(f"{DJ_KONG_ADMINAPI_BASEURI}/consumers/{email}/key-auth/").json()[
            "key"
        ]


def keycloak_account(email):
    token = ClientAccessToken.token_get()
    headers = {
        "Authorization": f"Bearer {token.access_token}",
        "Content-Type": "application/json",
    }
    new_user = {
        "username": email,
        "email": email,
        "enabled": "true",
        "credentials": [
            {
                "type": "password",
                "value": hashlib.md5(email).encode("utf-8").hexdigest()[-12:],
            },
            {"temporary": "true"},
        ],
    }
    rq.post(DJ_K_API_BASEURI + "/users/", headers=headers, json=new_user)


@receiver(signal=user_registered)
def oauth_provision_complete(request, sender, user, **kwargs):
    apikey = kong_apikey(user.email)
    keycloak_account(user.email)
    ApiKey.objects.create(key=apikey, user=user)


@login_required
def profile(request):
    try:
        T = UserAccessToken.objects.filter(user_id__exact=request.user.id).order_by(
            "-issued_at"
        )[0]
    except IndexError:
        T = UserAccessToken({"access_token": "None Generated"})
    return render(
        request,
        "kauthappusers/profile.html",
        {"token": T.access_token, "dt": str(T.issued_at)},
    )


def facebook_oauth(request):
    ...
