from django.contrib import admin

import catalog.models

__all__ = ["ItemAdmin"]

admin.site.register(catalog.models.Tag)
admin.site.register(catalog.models.Category)


class MainImageInline(admin.TabularInline):
    model = catalog.models.MainImage
    extra = 1
    verbose_name = "Изображение"
    verbose_name_plural = "Изображения"


@admin.register(catalog.models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.Item.main_image_tmb,
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
    )
    list_editable = (catalog.models.Item.is_published.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)
    filter_horizontal = (catalog.models.Item.tags.field.name,)
    inlines = [MainImageInline]
