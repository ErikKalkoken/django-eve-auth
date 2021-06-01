import logging

from django.conf import settings
from django.contrib import auth, messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from esi.decorators import token_required
from esi.models import Token

logger = logging.getLogger("__name__")


@token_required(new=True, scopes=settings.LOGIN_TOKEN_SCOPES)
def login(request, token):
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
            try:
                login_url = settings.LOGIN_SUCCESS_URL
            except KeyError:
                logger.warning("Settings not properly configured for django-eve-auth.")
                login_url = "/"
            return redirect(login_url)
        else:
            messages.warning(request, _("Your have been banned from this website."))
    else:
        messages.error(request, _("Unable to authenticate as the selected character."))
    return redirect(settings.LOGIN_URL)


def logout(request):
    """Logout current user."""
    auth.logout(request)
    try:
        logout_url = settings.LOGIN_URL
    except KeyError:
        logger.warning("Settings not properly configured for django-eve-auth.")
        logout_url = "/"
    return redirect(logout_url)
