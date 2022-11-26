from rest_framework import serializers
from .models import UserData, UserDataPoint, UserAccessToken


class UserDataSerializer(serializers.Serializer):
    class Meta:
        model = UserData
        exclude = ()


class UserDataPointSerializer(serializers.Serializer):
    class Meta:
        model = UserDataPoint
        exclude = ()


class AccessTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccessToken
        exclude = ()
