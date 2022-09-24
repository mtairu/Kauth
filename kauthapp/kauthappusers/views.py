from django.shortcuts import redirect, render
from django.forms.models import model_to_dict
from django.dispatch import receiver
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from core.settings import TOAuthConfig as OAUTHCONFIG

from registration.forms import RegistrationFormUniqueEmail
from registration.signals import user_registered
from kauthappusersapi.models import UserData, AccessToken


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
        return render(request, "kauthappusers/provision.html", context={"form": F})

    F = RegistrationFormUniqueEmail(request.POST)
    new_user = F.save()
    user_registered.send(sender=F.__class__, user=new_user, request=request)
    return redirect("/profile") 


@receiver(signal=user_registered)
def oauth_provision_complete(request, sender, user, **kwargs):
    if request.session.get("OAUTH_P"):
        UserData.objects.create(
            user=user,
            name=request.session["OAUTH_P"]["name"],
            email=request.session["OAUTH_P"]["email"],
            avatar=request.session["OAUTH_P"]["picture"],
        )
    else:
        UserData.objects.create(user=user, name=user.username, email=user.email)
    return HttpResponse()

@login_required
def profile(request):
    U = UserData.objects.get(email=request.user.email)
    try:
        T = AccessToken.objects.filter(email__startswith=request.user.email).order_by(
            "-issued_at"
        )[0]
    except Exception:
        T = AccessToken({"access_token": ""})
    return render(
        request,
        "kauthappusers/profile.html",
        {"data": model_to_dict(U), "token": model_to_dict(T)},
    )


def facebook_oauth(request):
    ...
