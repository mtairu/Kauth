import base64
from http import HTTPStatus
from django.contrib.auth import authenticate

from .models import UserData, UserDataPoint, AccessToken, Credential
from .serializers import (
    UserDataSerializer,
    UserDataPointSerializer,
    AccessTokenSerializer,
)
from rest_framework.decorators import action
from rest_framework.views import Response, exception_handler
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import APIException, AuthenticationFailed
from core.settings import TOAuthConfig as OAUTHCONFIG
import requests as rq


def get_creds():
    return Credential.objects.get(realm="KEYCLOAK")


def gen_token():
    """Generate token on keycloak on behalf of an authenticated user"""
    C = get_creds()
    payload = {
        "client_id": C.client_id,
        "client_secret": C.client_secret,
        "grant_type": "client_credentials",
    }
    resp = rq.post(OAUTHCONFIG.keycloak.token_uri, data=payload).json()
    return resp


class NotAllowedToViewException(APIException):
    status_code = 405
    default_detail = "Not Allowed"
    default_code = "Not Allowed"


class UserDataView(viewsets.ModelViewSet):
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer


class UserDataPointView(viewsets.ModelViewSet):
    queryset = UserDataPoint.objects.all()
    serializer_class = UserDataPointSerializer


class AccessTokenView(viewsets.ReadOnlyModelViewSet):
    queryset = AccessToken.objects.all()
    serializer_class = AccessTokenSerializer

    def list(self, request):
        raise NotAllowedToViewException

    def retrieve(self, request, pk):
        raise NotAllowedToViewException

    @action(detail=False)
    def tokens(self, request):
        if authorization := request.META.get("HTTP_AUTHORIZATION"):
            authorization = authorization.split(" ")[1]
            username, password = (
                base64.b64decode(authorization).decode("utf-8").split(":")
            )
        else:
            raise AuthenticationFailed()

        if U := authenticate(username=username, password=password):
            token = gen_token()
        else:
            raise AuthenticationFailed()

        AccessToken.objects.create(access_token=token["access_token"], user=U)
        return Response(token)


def api_exception_handler(exc: Exception, context):
    response = exception_handler(exc, context)

    if response is not None:
        http_code_to_message = {v.value: v.description for v in HTTPStatus}
        error_payload = {
            "error": {
                "status_code": 0,
                "message": "",
                "details": [],
            }
        }
        error = error_payload["error"]
        status_code = response.status_code
        error["status_code"] = status_code
        error["message"] = http_code_to_message[status_code]
        error["details"] = response.data
        response.data = error_payload
    return response
