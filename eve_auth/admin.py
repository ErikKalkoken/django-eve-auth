from typing import Optional

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    readonly_fields = ("character_id", "character_name", "character_owner_hash")


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_select_related = ("profile",)
    list_display = ("username", "_character_name", "is_staff")

    def _character_name(self, obj) -> Optional[str]:
        try:
            return obj.profile.character_name
        except (ObjectDoesNotExist, AttributeError):
            return None


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
