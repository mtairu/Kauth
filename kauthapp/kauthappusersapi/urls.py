from django.urls import include, path
from rest_framework import routers

from .views import UserDataView, UserDataPointView, AccessTokenView

router = routers.SimpleRouter()
router.register(r"users/userdata", UserDataView)
router.register(r"users/userdatapoints", UserDataPointView)
router.register(r"oauth", AccessTokenView)

urlpatterns = [
    path("", include(router.urls)),
]
