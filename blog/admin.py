from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ("name", "slug", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name_mk",)}


@admin.register(Post)
class PostAdmin(TranslationAdmin):
    list_display = ("title", "category", "author", "published_at", "is_published", "views")
    list_editable = ("is_published",)
    list_filter = ("is_published", "category", "author")
    search_fields = ("title", "excerpt", "body")
    prepopulated_fields = {"slug": ("title_mk",)}
    date_hierarchy = "published_at"
    list_select_related = ("category", "author")
    readonly_fields = ("views",)
