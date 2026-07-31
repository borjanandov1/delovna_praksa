import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView

from .forms import BookingForm, ContactForm

logger = logging.getLogger(__name__)


def notify_staff(subject, body):
    """
    Best-effort email notification.

    Wrapped in try/except on purpose: if SMTP is misconfigured or unreachable
    on the FCSE server, the visitor must still get their success page. The
    record is already safe in the database either way.
    """
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_NOTIFY_EMAIL],
            fail_silently=False,
        )
    except Exception:
        logger.exception("Failed to send notification email: %s", subject)


class HtmxFormMixin:
    """
    Progressive enhancement: without JS the form does a normal POST → redirect
    → success message (post/redirect/get, so a refresh can't double-submit).
    With HTMX it swaps in a success partial instead, no page reload.
    """

    success_partial = None
    success_message = ""

    def form_valid(self, form):
        self.object = form.save()
        self.after_save(self.object)

        if self.request.headers.get("HX-Request"):
            return render(
                self.request,
                self.success_partial,
                {"object": self.object, "success_message": self.success_message},
            )

        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get("HX-Request"):
            # Re-render just the form so HTMX can swap the errors back in.
            return render(
                self.request, self.form_partial, {"form": form}, status=422
            )
        return super().form_invalid(form)

    def after_save(self, obj):
        pass


class ContactView(HtmxFormMixin, CreateView):
    form_class = ContactForm
    template_name = "contact/contact.html"
    success_url = reverse_lazy("contact:contact")
    form_partial = "contact/partials/_contact_form.html"
    success_partial = "contact/partials/_contact_success.html"
    success_message = _("Thanks — your message has been sent. We'll reply shortly.")

    def after_save(self, obj):
        notify_staff(
            subject=f"[FORGE] New contact message: {obj.subject}",
            body=(
                f"From: {obj.name} <{obj.email}>\n"
                f"Phone: {obj.phone or '—'}\n\n"
                f"{obj.message}"
            ),
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["booking_form"] = BookingForm()
        return ctx


class BookingView(HtmxFormMixin, CreateView):
    form_class = BookingForm
    template_name = "contact/booking.html"
    success_url = reverse_lazy("contact:booking")
    form_partial = "contact/partials/_booking_form.html"
    success_partial = "contact/partials/_booking_success.html"
    success_message = _(
        "Booking received. We'll confirm your session by phone or email."
    )

    def after_save(self, obj):
        target = obj.gym_class.title if obj.gym_class else "Free trial session"
        notify_staff(
            subject=f"[FORGE] New booking: {target}",
            body=(
                f"Name: {obj.name}\n"
                f"Email: {obj.email}\n"
                f"Phone: {obj.phone}\n"
                f"Class: {target}\n"
                f"Date: {obj.preferred_date} {obj.preferred_time or ''}\n\n"
                f"{obj.notes}"
            ),
        )
