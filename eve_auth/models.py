from urllib.parse import urlencode, urljoin

from django.conf import settings
from django.db import models


class UserEveProfile(models.Model):
    """Eve profile for a user."""

    EVE_IMAGESERVER_URL_BASE = "https://images.evetech.net"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="eve_profile"
    )
    character_id = models.PositiveIntegerField(db_index=True)
    character_name = models.CharField(max_length=255, db_index=True)
    owner_hash = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.character_name

    def portrait_url(self, size: int = 32) -> str:
        """Return the image URL of the character's portrait"""
        size = int(size)
        if not size or size < 32 or size > 1024 or (size & (size - 1) != 0):
            raise ValueError(f"Invalid size: {size}")
        path = f"characters/{self.character_id}/portrait"
        query = urlencode({"size": size})
        return urljoin(self.EVE_IMAGESERVER_URL_BASE, f"{path}?{query}")
