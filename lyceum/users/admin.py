from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from users.models import Profile


__all__ = []


class ProfileInline(admin.TabularInline):
    model = Profile
    can_delete = False
    readonly_fields = [
        "birthday",
        "coffee_count",
        "image",
        "user",
    ]


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    readonly_fields = ["profile"]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
