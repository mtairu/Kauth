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
    queryset = UserData.objects.filter()
    serializer_class = UserDataSerializer

    def get_user(self, request):
        """
        Validate key/identifier

        Returns user object if valid, None otherwise

        todo:
            - rename, refactor
        """
        token = request.META.get("HTTP_TOKEN")
        return UserAccessToken.valid(token.split(".")[0]).user

    def create(self, request):
        user = self.get_user(request)
        content = request.data["content"]
        UserData.objects.create(user_id=user.id, content=content)
        return Response(status=201)

    def list(self, request):
        user = self.get_user(request)
        items = list(UserData.objects.filter(user_id=user.id).values("content", "id"))
        return Response(items)

    def destroy(self, request, pk=None):
        user = self.get_user(request)
        UserData.objects.filter(user_id=user.id, pk=pk).delete()
        return Response(status=204)


class UserDataPointView(viewsets.ModelViewSet):
    queryset = UserDataPoint.objects.all()
    serializer_class = UserDataPointSerializer

    def get_user(self, request):
        token = request.META.get("HTTP_TOKEN")
        return UserAccessToken.valid(token.split(".")[0]).user

    def create(self, request):
        user = self.get_user(request)
        content = request.data["content"]
        UserDataPoint.objects.create(user_id=user.id, content=content)
        return Response(status=201)

    def list(self, request):
        user = self.get_user(request)
        items = list(UserDataPoint.objects.filter(user_id=user).values("content", "id"))
        return Response(items)

    def destroy(self, request, pk=None):
        user = self.get_user(request)
        UserDataPoint.objects.filter(user_id=user.id, pk=pk).delete()
        return Response(status=204)


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
                identifier=token["access_token"].split(".")[0],
            )
            return Response(token)
        raise AuthenticationFailed()


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
