import dataclasses
from typing import Optional
import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from core.settings import TOAuthConfig as OAUTHCONFIG
import requests as rq


@dataclasses.dataclass
class TCredential:
    """Build credential obj"""

    bearer: dataclasses.InitVar[Optional[dict]] = None
    access_token: str = ""
    issued_at: datetime.datetime = timezone.now()
    expires: datetime.datetime = datetime.datetime.min
    is_expired = False

    def __post_init__(self, bearer: dict) -> None:
        if bearer:
            self.access_token = bearer["access_token"]
            self.expires = self.issued_at + timezone.timedelta(
                seconds=bearer["expires_in"]
            )

    def asdict(self) -> dict:
        return dataclasses.asdict(self)


def get_creds():
    return Credential.objects.get(realm="KEYCLOAK")


def client_credential() -> TCredential:
    """Manage authentication and retrival of tokens."""
    C = get_creds()
    req = rq.post(
        OAUTHCONFIG.keycloak.token_uri,
        data={
            "grant_type": "client_credentials",
            "client_id": C.client_id,
            "client_secret": C.client_secret,
        },
    )
    return TCredential(req.json())


class AccessToken(models.Model):
    access_token = models.TextField(unique=True, null=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    refresh_token = models.TextField(unique=True, null=True)
    expires = models.IntegerField(default=86400, unique=False)
    issued_at = models.DateTimeField(auto_now=True)


class Credential(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    client_id = models.CharField(max_length=255, null=False, unique=True)
    client_secret = models.CharField(max_length=255, null=False, unique=True)
    realm = models.CharField(default="KEYCLOAK", max_length=8, unique=True)

    def __str__(self):
        return self.user.email


class ClientAccessToken(models.Model):
    access_token = models.TextField(unique=True, null=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    refresh_token = models.TextField(unique=True, null=True)
    issued_at = models.DateTimeField(auto_now=True)
    expires = models.DateTimeField()
    is_expired = models.BooleanField(default=False)

    @classmethod
    def token_save(cls, c, user):
        return cls.objects.create(
            user=user,
            access_token=c.access_token,
            issued_at=c.issued_at,
            expires=c.expires,
        )

    @classmethod
    def token_get(cls):
        try:
            token = cls.objects.get(is_expired=False)
        except Exception:
            token = TCredential()

        if timezone.now() > token.expires:
            token.is_expired = True
            token.save()
            new_token = client_credential()
            cls.token_save(new_token, token.user)
            return new_token
        return token


class UserData(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.name


class UserDataPoint(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.name
