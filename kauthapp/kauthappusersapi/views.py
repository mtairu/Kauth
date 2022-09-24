from typing import Any
from http import HTTPStatus
from .models import UserData, UserDataPoint, AccessToken
from .serializers import (
    UserDataSerializer,
    UserDataPointSerializer,
    AccessTokenSerializer,
)

from rest_framework.views import Response, exception_handler
from rest_framework import viewsets
from rest_framework.response import Response
import requests as rq
from core.settings import TOAuthConfig as OAUTHCONFIG
from rest_framework.exceptions import APIException


class UserDataView(viewsets.ModelViewSet):
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer


class UserDataPointView(viewsets.ModelViewSet):
    queryset = UserDataPoint.objects.all()
    serializer_class = UserDataPointSerializer


class AccessTokenView(viewsets.ModelViewSet):
    queryset = AccessToken.objects.all()
    serializer_class = AccessTokenSerializer

    def retrieve(self, request):
        ...

    def list(self, request):
        ...

    def create(self, request):
        try:
            U = UserData.objects.get(email=request.data.get("email"))
        except Exception as err:
            raise APIException(err)

        payload = {
            "client_id": OAUTHCONFIG.keycloak.client_id,
            "client_secret": OAUTHCONFIG.keycloak.client_secret,
            "grant_type": "client_credentials",
        }
        resp = rq.post(OAUTHCONFIG.keycloak.token_uri, data=payload).json()
        AccessToken.objects.create(
            user=U.user,
            email=request.data.get("email"),
            access_token=resp["access_token"],
        )
        return Response(resp)


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
