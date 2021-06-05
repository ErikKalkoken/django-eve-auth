import secrets
import string

from django.contrib.auth.models import User
from esi.models import Token

from ..backends import EveSSOBackend


def create_fake_token(
    character_id: int,
    character_name: str,
    user: User = None,
    character_owner_hash: str = None,
) -> Token:
    """Create a fake token."""
    if not character_owner_hash:
        character_owner_hash = random_string(28)
    return Token.objects.create(
        access_token=random_string(28),
        refresh_token=random_string(28),
        user=user,
        character_id=character_id,
        character_name=character_name,
        character_owner_hash=character_owner_hash,
    )


def create_fake_user(
    character_id: int, character_name: str, owner_hash: str = None
) -> User:
    """Create fake user from given eve character details."""
    token = create_fake_token(
        character_id=character_id,
        character_name=character_name,
        character_owner_hash=owner_hash,
    )
    user = EveSSOBackend.create_user_from_token(token)
    token.user = user
    token.save()
    return user


def random_string(length: int) -> int:
    """Create random string consisting of lower case ascii characters and digits."""
    return "".join(
        secrets.choice(string.ascii_lowercase + string.digits) for _ in range(length)
    )
