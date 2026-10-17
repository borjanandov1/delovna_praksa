from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Specialty, TeamMember


@admin.register(Specialty)
class SpecialtyAdmin(TranslationAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name_mk",)}
    search_fields = ("name",)


@admin.register(TeamMember)
class TeamMemberAdmin(TranslationAdmin):
    list_display = ("name", "role", "years_experience", "is_active", "order")
    list_editable = ("is_active", "order")
    list_filter = ("is_active", "specialties")
    search_fields = ("name", "role", "bio")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("specialties",)
