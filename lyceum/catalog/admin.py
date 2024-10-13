import catalog.models

from django.contrib import admin

admin.site.register(catalog.models.Tag)
admin.site.register(catalog.models.Category)


@admin.register(catalog.models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
    )
    list_editable = ("is_published",)
    list_display_links = ("name",)
    filter_horizontal = (catalog.models.Item.tags.field.name,)
