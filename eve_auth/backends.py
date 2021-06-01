import logging
import re

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from esi.models import Token

from .models import UserEveProfile

logger = logging.getLogger(__name__)


class EveSSOBackend(BaseBackend):
    def authenticate(self, request, token=None) -> object:
        """Authenticate user with Eve token."""
        if not isinstance(token, Token):
            return None
        User = get_user_model()
        try:
            user = User.objects.get(eve_profile__owner_hash=token.character_owner_hash)
        except User.DoesNotExist:
            user = self.create_user_from_eve_character(
                character_id=token.character_id,
                charater_name=token.character_name,
                owner_hash=token.character_owner_hash,
            )
        return user

    @classmethod
    def create_user_from_eve_character(
        cls, character_id: int, charater_name: str, owner_hash: str
    ) -> object:
        """Create new user object with eve profile from an eve character."""
        username = cls._clean_username(charater_name)
        first_name, last_name = cls._first_and_last_name(charater_name)
        user = get_user_model().objects.create(
            username=cls._generate_username(username),
            first_name=first_name,
            last_name=last_name,
        )
        UserEveProfile.objects.create(
            user=user,
            character_id=character_id,
            character_name=charater_name,
            owner_hash=owner_hash,
        )
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
