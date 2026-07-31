from django.db import models
from django.utils.translation import gettext_lazy as _


class ContactMessage(models.Model):
    name = models.CharField(_("name"), max_length=120)
    email = models.EmailField(_("email"))
    phone = models.CharField(_("phone"), max_length=40, blank=True)
    subject = models.CharField(_("subject"), max_length=200)
    message = models.TextField(_("message"))

    created_at = models.DateTimeField(_("received"), auto_now_add=True)
    is_read = models.BooleanField(_("read"), default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("contact message")
        verbose_name_plural = _("contact messages")

    def __str__(self):
        return f"{self.name} — {self.subject}"


class Booking(models.Model):
    """A trial-session / class booking request. Confirmed manually by staff."""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    STATUSES = [
        (PENDING, _("Pending")),
        (CONFIRMED, _("Confirmed")),
        (CANCELLED, _("Cancelled")),
    ]

    name = models.CharField(_("name"), max_length=120)
    email = models.EmailField(_("email"))
    phone = models.CharField(_("phone"), max_length=40)

    gym_class = models.ForeignKey(
        "training.GymClass",
        verbose_name=_("class"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings",
    )
    preferred_date = models.DateField(_("preferred date"))
    preferred_time = models.TimeField(_("preferred time"), null=True, blank=True)
    notes = models.TextField(_("notes"), blank=True)

    status = models.CharField(
        _("status"), max_length=12, choices=STATUSES, default=PENDING
    )
    created_at = models.DateTimeField(_("created"), auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("booking")
        verbose_name_plural = _("bookings")

    def __str__(self):
        target = self.gym_class.title if self.gym_class else _("trial session")
        return f"{self.name} — {target} ({self.preferred_date})"
