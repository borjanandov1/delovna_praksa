from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline

from .models import Service, ServiceCategory, ServiceImage


class ServiceImageInline(TranslationStackedInline):
    model = ServiceImage
    extra = 1


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(TranslationAdmin):
    list_display = ("name", "slug", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Service)
class ServiceAdmin(TranslationAdmin):
    list_display = ("title", "category", "price_from", "duration_min", "is_featured", "order")
    list_editable = ("is_featured", "order")
    list_filter = ("category", "is_featured")
    search_fields = ("title", "short_desc", "full_desc")
    prepopulated_fields = {"slug": ("title_mk",)}
    inlines = [ServiceImageInline]
    list_select_related = ("category",)
