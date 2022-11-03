from http import HTTPStatus

from rest_framework.decorators import action
from rest_framework.views import Response, exception_handler
from rest_framework import viewsets
from rest_framework.exceptions import APIException, AuthenticationFailed
from kauthappusers.services import keycloak_access_token
from kauthappusersapi.models import UserData, UserDataPoint, UserAccessToken, ApiKey

from .serializers import (
    UserDataSerializer,
    UserDataPointSerializer,
    AccessTokenSerializer,
)


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
    queryset = UserAccessToken.objects.all()
    serializer_class = AccessTokenSerializer

    def list(self, request):
        raise NotAllowedToViewException

    def retrieve(self, request, pk):
        raise NotAllowedToViewException

    @action(detail=False)
    def tokens(self, request):
        apikey = request.META.get("HTTP_APIKEY")
        if valid := ApiKey.valid(apikey):
            token = keycloak_access_token()
            UserAccessToken.objects.create(
                access_token=token["access_token"],
                user=valid.user,
            )
            return Response(token)
        raise ApiKey.DoesNotExist


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
