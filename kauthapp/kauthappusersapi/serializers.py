from rest_framework.serializers import ModelSerializer
from .models import UserData, UserDataPoint, UserAccessToken


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
        model = UserAccessToken
        exclude = ()
