import django.contrib.admin
import django.contrib.auth.admin
import django.contrib.auth.models

import users.models


__all__ = []


class ProfileInline(django.contrib.admin.TabularInline):
    model = users.models.Profile
    can_delete = False
    readonly_fields = (users.models.Profile.image_tmb,)


class UserAdmin(django.contrib.auth.admin.UserAdmin):
    inlines = (ProfileInline,)


django.contrib.admin.site.unregister(django.contrib.auth.models.User)
django.contrib.admin.site.register(django.contrib.auth.models.User, UserAdmin)
