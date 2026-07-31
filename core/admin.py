from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from .models import FAQ, OpeningHours, SiteSettings, Testimonial

admin.site.site_header = "FORGE Fitness Studio"
admin.site.site_title = "FORGE admin"
admin.site.index_title = _("Manage the website")


@admin.register(SiteSettings)
class SiteSettingsAdmin(TranslationAdmin):
    fieldsets = (
        (_("Identity"), {"fields": ("name", "tagline", "short_about", "logo", "hero_image")}),
        (_("Address"), {"fields": ("street", "postal_code", "city")}),
        (_("Contact"), {"fields": ("phone", "email")}),
        (_("Social media"), {"fields": ("facebook", "instagram", "youtube")}),
        (_("Map"), {"fields": ("map_lat", "map_lng")}),
    )

    def has_add_permission(self, request):
        # Singleton: exactly one row, created on first access.
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(OpeningHours)
class OpeningHoursAdmin(admin.ModelAdmin):
    list_display = ("get_weekday_display", "opens", "closes", "is_closed")
    list_editable = ("opens", "closes", "is_closed")
    list_display_links = ("get_weekday_display",)
    ordering = ("weekday",)


@admin.register(Testimonial)
class TestimonialAdmin(TranslationAdmin):
    list_display = ("author", "role", "rating", "is_featured", "order")
    list_editable = ("is_featured", "order")
    list_filter = ("is_featured", "rating")
    search_fields = ("author", "text")


@admin.register(FAQ)
class FAQAdmin(TranslationAdmin):
    list_display = ("question", "category", "order")
    list_editable = ("category", "order")
    list_filter = ("category",)
    search_fields = ("question", "answer")
