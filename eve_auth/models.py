from urllib.parse import urlencode, urljoin

from django.conf import settings
from django.db import models
from esi.models import Token


class UserEveProfile(models.Model):
    """Eve profile for a user."""

    CHARACTER_IMAGE_URL_BASE = "https://images.evetech.net/characters/"
    DEFAULT_PORTRAIT_SIZE = 32

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="eve_profile"
    )
    token = models.OneToOneField(
        Token, on_delete=models.CASCADE, related_name="eve_profile"
    )

    def __str__(self) -> str:
        return self.character_name

    @property
    def character_id(self):
        return self.token.character_id

    @property
    def character_name(self):
        return self.token.character_name

    def character_portrait_url(self, size: int = DEFAULT_PORTRAIT_SIZE) -> str:
        """Return the image URL of the user's character portrait"""
        return self.generic_character_portrait_url(self.character_id, size)

    @classmethod
    def generic_character_portrait_url(
        cls, character_id: int, size: int = DEFAULT_PORTRAIT_SIZE
    ) -> str:
        """Return the image URL of the given character's portrait"""
        size = int(size)
        if not size or size < 32 or size > 1024 or (size & (size - 1) != 0):
            raise ValueError(f"Invalid size: {size}")
        path = f"{int(character_id)}/portrait"
        query = urlencode({"size": size})
        return urljoin(cls.CHARACTER_IMAGE_URL_BASE, f"{path}?{query}")
