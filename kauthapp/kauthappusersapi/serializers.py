from rest_framework.serializers import ModelSerializer
from .models import UserData, UserDataPoint, AccessToken


class UserDataSerializer(ModelSerializer):
    class Meta:
        model = UserData
        exclude = ()


class UserDataPointSerializer(ModelSerializer):
    class Meta:
        model = UserDataPoint
        exclude = ()


class AccessTokenSerializer(ModelSerializer):
    class Meta:
        model = AccessToken
        exclude = ()
