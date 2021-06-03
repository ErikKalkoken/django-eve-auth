from typing import Optional

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from .models import UserEveProfile


class UserEveProfileInline(admin.StackedInline):
    model = UserEveProfile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (UserEveProfileInline,)

    list_select_related = True
    list_display = ("username", "_charater_name", "is_staff")

    def _charater_name(self, obj) -> Optional[str]:
        try:
            return obj.eve_profile.character_name
        except (ObjectDoesNotExist, AttributeError):
            return None


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
