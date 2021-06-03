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

    list_display = ("username", "_character_name", "is_staff")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("eve_profile__token")

    def _character_name(self, obj) -> Optional[str]:
        try:
            return obj.eve_profile.character_name
        except (ObjectDoesNotExist, AttributeError):
            return None


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
