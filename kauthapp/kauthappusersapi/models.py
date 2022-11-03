import base64

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import requests as rq

from core.settings import TOAuthConfig as OAUTHCONFIG
from kauthappusersapi.typedefs import TCredential


class OauthClient(models.Model):
    """
    Manages Credentials for Keycloak clients
    """

    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    client_id = models.CharField(max_length=255, null=False, unique=True)
    client_secret = models.CharField(max_length=255, null=False, unique=True)
    realm = models.CharField(default="KEYCLOAK", max_length=8, unique=True)

    def __str__(self):
        return self.user.email

    @classmethod
    def basic_credential(cls):
        """Return a Keycloak client's credential in base64"""
        C = cls.objects.get(realm=OAUTHCONFIG.realm)
        credential = base64.b64encode(
            f"{C.client_id}:{C.client_secret}".encode("utf-8")
        )
        return credential.decode()


class UserAccessToken(models.Model):
    """
    Manages access tokens for Keycloak users
    Rename to OauthUserToken
    """

    access_token = models.TextField(unique=True, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    refresh_token = models.TextField(unique=True, null=True)
    expires = models.IntegerField(default=86400, unique=False)
    is_expired = models.BooleanField(default=False)
    issued_at = models.DateTimeField(auto_now=True)


class ClientAccessToken(models.Model):
    """
    Manages access tokens for Keycloak client
    Rename to OauthClientToken
    """

    access_token = models.TextField(unique=True, null=False)
    refresh_token = models.TextField(unique=True, null=True)
    issued_at = models.DateTimeField(auto_now=True)
    expires = models.DateTimeField()
    is_expired = models.BooleanField(default=False)
    client = models.ForeignKey(OauthClient, on_delete=models.CASCADE)

    @classmethod
    def client_access_token(cls) -> TCredential:
        """
        Request client access token from Keycloak server

        todo:
        - Move to services.py
        """
        C = OauthClient.objects.get(realm=OAUTHCONFIG.realm)

        req = rq.post(
            OAUTHCONFIG.keycloak.token_uri,
            data={
                "grant_type": "client_credentials",
                "client_id": C.client_id,
                "client_secret": C.client_secret,
            },
        )
        return TCredential(req.json(), client=C)

    @classmethod
    def token_save(cls, c: TCredential):
        """Save a new token"""
        return cls.objects.create(
            access_token=c.access_token,
            issued_at=c.issued_at,
            client=c.client,
            expires=c.expires,
        )

    @classmethod
    def token_get(cls):

        try:
            token = cls.objects.get(is_expired=False)
        except cls.DoesNotExist:
            new_token = cls.client_access_token()
            return cls.token_save(new_token)

        if timezone.now() > token.expires:
            token.is_expired = True
            token.save()
            new_token = cls.client_access_token()
            return cls.token_save(new_token)
        return token


class ApiKey(models.Model):
    """
    Manages APIKEYS from Kong
    Keys are credentials for users to generate accesstokens.
    """

    key = models.CharField(null=False, max_length=255, unique=True)
    issued_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.user.email

    @classmethod
    def valid(cls, key: str):
        return cls.objects.filter(key=key).first()


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
