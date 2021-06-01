from django.conf import settings
from django.db import models


class UserEveProfile(models.Model):
    """Eve profile for a user."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="eve_profile"
    )
    character_id = models.PositiveIntegerField(db_index=True)
    character_name = models.CharField(max_length=255, db_index=True)
    owner_hash = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.character_name

    def portrait_url(self, size=32) -> str:
        """Return the image URL of the character's portrait"""
        try:
            size = int(size)
        except TypeError:
            size = 32
        return (
            f"https://images.evetech.net/characters/{self.character_id}/portrait"
            f"?size={size}"
        )
