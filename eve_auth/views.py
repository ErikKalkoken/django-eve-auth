import logging

from django.contrib import auth, messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from esi.decorators import token_required
from esi.models import Token

from . import app_settings

logger = logging.getLogger("__name__")


@token_required(new=True, scopes=app_settings.EVE_AUTH_LOGIN_SCOPES)
def login(request, token: Token):
    """Login user with authorization from EVE SSO."""
    user = auth.authenticate(token=token)
    if user:
        token.user = user
        if (
            Token.objects.exclude(pk=token.pk)
            .equivalent_to(token)
            .require_valid()
            .exists()
        ):
            token.delete()
        else:
            token.save()
        if user.is_active:
            auth.login(request, user)
            return redirect(app_settings.EVE_AUTH_LOGIN_SUCCESS_URL)
        else:
            messages.warning(request, _("Your have been banned from this website."))
    else:
        messages.error(request, _("Unable to authenticate as the selected character."))
    return redirect(app_settings.EVE_AUTH_LOGIN_URL)


def logout(request):
    """Logout current user."""
    auth.logout(request)
    return redirect(app_settings.EVE_AUTH_LOGIN_URL)
