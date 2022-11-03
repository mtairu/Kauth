import dataclasses
import hashlib

from django.http import HttpResponse
import requests as rq
from requests.exceptions import ConnectionError
from core.settings import (
    DJ_K_API_BASEURI,
    DJ_KONG_ADMINAPI_BASEURI,
    DJ_KONG_ADMINAPI_KEY,
)

from kauthappusersapi.models import ClientAccessToken


@dataclasses.dataclass
class TKongResponse:
    status_code: str
    content: str


def kong_create_consumer(email: str):
    """
    Add a user to Kong Gateway as a consumer
    https://docs.konghq.com/gateway/latest/admin-api/#consumer-object
    """
    resp = rq.post(
        f"{DJ_KONG_ADMINAPI_BASEURI}/consumers/",
        json={"username": email},
        timeout=3.0,
        headers={"apikey": DJ_KONG_ADMINAPI_KEY},
    )
    if resp.status_code != 201:
        raise ConnectionError(resp.status_code, resp.json())
    return TKongResponse(status_code=resp.status_code, content=resp)


def kong_consumer_apikey(email):
    """
    Request for an APIKEY for a user (consumer) on KongGateway
    """
    resp = rq.post(
        f"{DJ_KONG_ADMINAPI_BASEURI}/consumers/{email}/key-auth/",
        timeout=3.0,
        headers={"apikey": DJ_KONG_ADMINAPI_KEY},
    )
    if resp.status_code != 201:
        raise ConnectionError(resp.status_code, resp.json())
    return TKongResponse(status_code=resp.status_code, content=resp)


def keycloak_account(email):
    token = ClientAccessToken.token_get()
    headers = {
        "Authorization": f"Bearer {token.access_token}",
        "Content-Type": "application/json",
    }
    new_user = {
        "username": email,
        "email": email,
        "enabled": "true",
        "credentials": [
            {
                "type": "password",
                "value": hashlib.md5(bytes(email, "utf-8")).hexdigest()[-12:],
            },
            {"temporary": "true"},
        ],
    }
    return rq.post(DJ_K_API_BASEURI + "/users/", headers=headers, json=new_user)
