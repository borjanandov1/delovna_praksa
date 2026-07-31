from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from training.models import GymClass

from .models import Booking, ContactMessage


class HoneypotMixin:
    """
    Adds a decoy field that real users never see (moved off-screen by CSS, not
    display:none — some bots skip hidden fields). If it comes back filled in,
    the submission is a bot.

    Deliberately not a captcha: the assignment forbids nothing here, but a
    captcha would add a third-party dependency and hurt accessibility.
    """

    HONEYPOT = "website"

    def _add_honeypot(self):
        self.fields[self.HONEYPOT] = forms.CharField(
            required=False,
            label=_("Leave this field empty"),
            widget=forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "tabindex": "-1",
                    "class": "hp-field",
                    "aria-hidden": "true",
                }
            ),
        )

    def clean(self):
        cleaned = super().clean()
        if cleaned.get(self.HONEYPOT):
            raise forms.ValidationError(_("Your submission could not be processed."))
        return cleaned


class ContactForm(HoneypotMixin, forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "subject", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": _("Your name"), "autocomplete": "name"}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "you@example.com", "autocomplete": "email"}
            ),
            "phone": forms.TextInput(
                attrs={"placeholder": "+389 7X XXX XXX", "autocomplete": "tel"}
            ),
            "subject": forms.TextInput(attrs={"placeholder": _("How can we help?")}),
            "message": forms.Textarea(attrs={"rows": 5, "placeholder": _("Your message")}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._add_honeypot()
        self.fields["phone"].required = False

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 10:
            raise forms.ValidationError(
                _("Please write at least 10 characters so we can help properly.")
            )
        return message


class BookingForm(HoneypotMixin, forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "name",
            "email",
            "phone",
            "gym_class",
            "preferred_date",
            "preferred_time",
            "notes",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"autocomplete": "tel"}),
            "preferred_date": forms.DateInput(
                attrs={"type": "date"}, format="%Y-%m-%d"
            ),
            "preferred_time": forms.TimeInput(attrs={"type": "time"}, format="%H:%M"),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._add_honeypot()
        self.fields["gym_class"].queryset = GymClass.objects.filter(is_active=True)
        self.fields["gym_class"].empty_label = _("Free trial session (any class)")
        self.fields["gym_class"].required = False
        # Stop the browser offering past dates in the native picker.
        self.fields["preferred_date"].widget.attrs["min"] = timezone.localdate().isoformat()

    def clean_preferred_date(self):
        date = self.cleaned_data["preferred_date"]
        if date < timezone.localdate():
            raise forms.ValidationError(_("Please choose a date in the future."))
        return date
