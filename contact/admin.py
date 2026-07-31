from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Booking, ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_read")
    list_editable = ("is_read",)
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    date_hierarchy = "created_at"
    readonly_fields = ("name", "email", "phone", "subject", "message", "created_at")
    actions = ["mark_read", "mark_unread"]

    def has_add_permission(self, request):
        # Messages only ever arrive through the public form.
        return False

    @admin.action(description=_("Mark selected messages as read"))
    def mark_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description=_("Mark selected messages as unread"))
    def mark_unread(self, request, queryset):
        queryset.update(is_read=False)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("name", "gym_class", "preferred_date", "preferred_time", "status", "created_at")
    list_editable = ("status",)
    list_filter = ("status", "preferred_date", "gym_class")
    search_fields = ("name", "email", "phone")
    date_hierarchy = "preferred_date"
    readonly_fields = ("created_at",)
    list_select_related = ("gym_class",)
    actions = ["confirm", "cancel"]

    @admin.action(description=_("Confirm selected bookings"))
    def confirm(self, request, queryset):
        queryset.update(status=Booking.CONFIRMED)

    @admin.action(description=_("Cancel selected bookings"))
    def cancel(self, request, queryset):
        queryset.update(status=Booking.CANCELLED)
