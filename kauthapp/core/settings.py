"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import ast
from pathlib import Path
from os import environ
import dataclasses

# Build paths inside the project like this: BASE_DIR / 'subdir'.
HOSTNAME_STRICT = environ["DJ_HOSTNAME_STRICT"]
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = environ.get("DJ_SECRET_KEY")
DEBUG = ast.literal_eval(str(environ.get("DJ_DEBUG")))
ALLOWED_HOSTS = [environ.get("DJ_ALLOWED_HOSTS")]
CSRF_TRUSTED_ORIGINS = [HOSTNAME_STRICT]
DJ_K_API_BASEURI = environ["DJ_K_API_BASEURI"]
DJ_KONG_ADMINAPI_BASEURI = environ["DJ_KONG_ADMINAPI_BASEURI"]
DJ_KONG_ADMINAPI_KEY = environ["DJ_KONG_ADMINAPI_KEY"]

# Application definition

INSTALLED_APPS = [
    "registration",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "kauthappusers.apps.KauthappusersConfig",
    "rest_framework",
    "kauthappusersapi.apps.KauthappusersapiConfig",
    "drf_standardized_errors",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": environ.get("DJ_DB_NAME"),
        "USER": environ.get("DJ_DB_USER"),
        "PASSWORD": environ.get("DJ_DB_PASS"),
        "HOST": environ.get("DJ_DB_HOST"),
        "PORT": "5432",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# Registration redux
REGISTRATION_OPEN = True
REGISTRATION_AUTO_LOGIN = False
LOGIN_REDIRECT_URL = "/profile"

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "kauthappusersapi.views.api_exception_handler",
}
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# OAuth & OIDC
@dataclasses.dataclass
class TGOAuthCredentials:
    auth_uri: str = environ["DJ_G_AUTH_URI"]
    token_uri: str = environ["DJ_G_TOKEN_URI"]
    client_id: str = environ["DJ_G_CLIENT_ID"]
    client_secret: str = environ["DJ_G_CLIENT_SEC"]
    scopes = [
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
    ]


@dataclasses.dataclass
class TKeycloak:
    token_uri: str = environ["DJ_K_TOKEN_URI"]
    token_rovoke_uri: str = environ["DJ_K_TOKEN_REVOKE_URI"]


@dataclasses.dataclass
class TOAuthConfig:
    google: TGOAuthCredentials = TGOAuthCredentials
    callback_path: str = "/oauth2callback"
    hostname_strict: str = HOSTNAME_STRICT
    keycloak: TKeycloak = TKeycloak
    realm: str = environ["DJ_K_REALM"]
