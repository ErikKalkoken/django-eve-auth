from django.conf import settings

try:
    LOGIN_TOKEN_SCOPES = str(settings.LOGIN_TOKEN_SCOPES)
except AttributeError:
    LOGIN_TOKEN_SCOPES = ""

try:
    LOGIN_URL = str(settings.LOGIN_URL)
except AttributeError:
    LOGIN_URL = "/"

try:
    LOGIN_SUCCESS_URL = str(settings.LOGIN_SUCCESS_URL)
except AttributeError:
    LOGIN_SUCCESS_URL = "/"
