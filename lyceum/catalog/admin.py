import catalog.models
from django.contrib import admin

admin.site.register(catalog.models.Tag)
admin.site.register(catalog.models.Category)


@admin.register(catalog.models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_published",
    )
    list_editable = ("is_published",)
    list_display_links = ("name",)
    filter_horizontal = ("tags",)
