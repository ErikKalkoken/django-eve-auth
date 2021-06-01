from django.conf import settings

try:
    EVE_AUTH_LOGIN_SCOPES = str(settings.EVE_AUTH_LOGIN_SCOPES)
except AttributeError:
    EVE_AUTH_LOGIN_SCOPES = ""

try:
    EVE_AUTH_LOGIN_URL = str(settings.EVE_AUTH_LOGIN_URL)
except AttributeError:
    EVE_AUTH_LOGIN_URL = "/"

try:
    EVE_AUTH_LOGIN_SUCCESS_URL = str(settings.EVE_AUTH_LOGIN_SUCCESS_URL)
except AttributeError:
    EVE_AUTH_LOGIN_SUCCESS_URL = "/"

try:
    EVE_AUTH_USER_ICON_DEFAULT_SIZE = str(settings.EVE_AUTH_USER_ICON_DEFAULT_SIZE)
except AttributeError:
    EVE_AUTH_USER_ICON_DEFAULT_SIZE = 24
