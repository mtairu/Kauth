from django.db import models
from django.contrib.auth.models import User


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


# Create your models here.
