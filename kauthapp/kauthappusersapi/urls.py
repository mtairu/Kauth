from django.urls import include, path
from rest_framework import routers

from .views import UserDataView, UserDataPointView, AccessTokenView

router = routers.SimpleRouter()
router.register(r"userdata", UserDataView)
router.register(r"userdatapoints", UserDataPointView)
router.register(r"oauth/tokens", AccessTokenView)

urlpatterns = [
    path("", include(router.urls)),
]
