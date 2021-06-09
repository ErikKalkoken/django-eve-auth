import logging
import re

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from esi.models import Token

from .models import UserEveCharacter

logger = logging.getLogger(__name__)


class EveSSOBackend(BaseBackend):
    def authenticate(self, request, token: Token = None) -> User:
        """Authenticate user with Eve token."""
        if not isinstance(token, Token):
            return None
        if token.expired:
            logger.info("Can not authenticate with expired Eve SSO token")
            return None
        User = get_user_model()
        try:
            user = User.objects.get(
                eve_character__character_owner_hash=token.character_owner_hash
            )
        except User.DoesNotExist:
            user = self.create_user_from_token(token)
        else:
            logger.info("Authenticated user %s with Eve SSO token", user)
            user.eve_character.character_name = token.character_name
            user.eve_character.save()
        return user

    @classmethod
    def create_user_from_token(cls, token: Token) -> object:
        """Create new user object from an ESI token."""
        username = cls._clean_username(token.character_name)
        first_name, last_name = cls._first_and_last_name(token.character_name)
        user = get_user_model().objects.create(
            username=cls._generate_username(username),
            first_name=first_name,
            last_name=last_name,
        )
        UserEveCharacter.objects.create(
            user=user,
            character_id=token.character_id,
            character_name=token.character_name,
            character_owner_hash=token.character_owner_hash,
        )
        logger.info("Created new user %s from Eve SSO token", user)
        return user

    @staticmethod
    def _clean_username(name: str) -> str:
        """Return cleaned name containing only valid character for a username."""
        return re.sub(r"[^\w\d@\.\+-]", "_", name)

    @staticmethod
    def _generate_username(username) -> str:
        """Generate and return unique username from given username."""
        User = get_user_model()
        username_2 = username
        n = 0
        while User.objects.filter(username=username_2).exists():
            n += 1
            username_2 = f"{username}_{n}"
        return username_2

    @staticmethod
    def _first_and_last_name(fullname: str) -> tuple:
        parts = fullname.split(" ")
        last_name = parts.pop()
        first_name = " ".join(parts)
        return first_name, last_name

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
