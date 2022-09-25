from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from core.settings import TOAuthConfig as OAUTHCONFIG

from registration.forms import RegistrationFormUniqueEmail

from requests_oauthlib import OAuth2Session


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
        return render(
            request,
            "kauthappusers/provision.html",
            context={"form": F},
        )

    F = RegistrationFormUniqueEmail(request.POST)
    F.save()
    return redirect("/profile")


@login_required
def profile(request):
    return render(request, "kauthappusers/profile.html")


def facebook_oauth(request):
    ...
