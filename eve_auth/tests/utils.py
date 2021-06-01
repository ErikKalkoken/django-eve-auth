import secrets
import string

from django.contrib.auth.models import User

from ..backends import EveSSOBackend


def create_fake_user(
    character_id: int, character_name: str, owner_hash: str = None
) -> User:
    """Create fake user from given eve character details."""
    if not owner_hash:
        owner_hash = random_string(28)
    return EveSSOBackend.create_user_from_eve_character(
        character_id=character_id, charater_name=character_name, owner_hash=owner_hash
    )


def random_string(length: int) -> int:
    """Create random string consisting of lower case ascii characters and digits."""
    return "".join(
        secrets.choice(string.ascii_lowercase + string.digits) for _ in range(length)
    )
