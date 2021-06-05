import logging

from django.conf import settings
from django.contrib import auth, messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from esi.decorators import token_required
from esi.models import Token

from . import app_settings
from .decorators import remember_previous_page

logger = logging.getLogger("__name__")

LAST_PAGE_BEFORE_LOGIN = "last_page_before_login"
LAST_PAGE_BEFORE_LOGOUT = "last_page_before_logout"


@remember_previous_page(LAST_PAGE_BEFORE_LOGIN)
@token_required(new=True, scopes=app_settings.EVE_AUTH_LOGIN_SCOPES)
def login(request, token: Token):
    """Login user with authorization from EVE SSO."""
    last_page_url = request.session.get(LAST_PAGE_BEFORE_LOGIN)
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
            logger.debug("last page url: %s", last_page_url)
            return (
                redirect(last_page_url)
                if last_page_url
                else redirect(settings.LOGIN_REDIRECT_URL)
            )
        else:
            messages.warning(request, _("Your have been banned from this website."))
    else:
        messages.error(request, _("Unable to authenticate as the selected character."))
    return redirect(last_page_url) if last_page_url else redirect(settings.LOGIN_URL)


@remember_previous_page(LAST_PAGE_BEFORE_LOGOUT)
def logout(request):
    """Logout current user."""
    last_page_url = request.session.get(LAST_PAGE_BEFORE_LOGOUT)
    auth.logout(request)
    return redirect(last_page_url) if last_page_url else redirect(settings.LOGIN_URL)
