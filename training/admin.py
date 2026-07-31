from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline

from .models import ClassSession, GymClass, MembershipPlan


class ClassSessionInline(TranslationTabularInline):
    model = ClassSession
    extra = 2
    # Editing the weekly slots inline is what makes the timetable manageable
    # for the gym owner — one screen per class instead of a separate model.


@admin.register(GymClass)
class GymClassAdmin(TranslationAdmin):
    list_display = ("title", "trainer", "intensity", "duration_min", "capacity", "is_active", "order")
    list_editable = ("is_active", "order")
    list_filter = ("intensity", "is_active", "trainer")
    search_fields = ("title", "short_desc", "full_desc")
    prepopulated_fields = {"slug": ("title_mk",)}
    inlines = [ClassSessionInline]
    list_select_related = ("trainer",)


@admin.register(ClassSession)
class ClassSessionAdmin(TranslationAdmin):
    list_display = ("gym_class", "get_weekday_display", "start_time", "room")
    list_filter = ("weekday", "gym_class")
    ordering = ("weekday", "start_time")
    list_select_related = ("gym_class",)


@admin.register(MembershipPlan)
class MembershipPlanAdmin(TranslationAdmin):
    list_display = ("name", "price", "period", "is_featured", "order")
    list_editable = ("price", "is_featured", "order")
    prepopulated_fields = {"slug": ("name_mk",)}
