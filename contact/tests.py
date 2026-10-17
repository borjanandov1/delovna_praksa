from datetime import timedelta

from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from training.models import GymClass

from .models import Booking, ContactMessage

VALID_CONTACT = {
    "name": "Ивана Ристеска",
    "email": "ivana@example.com",
    "phone": "+389 70 123 456",
    "subject": "Прашање за членство",
    "message": "Дали има попуст за студенти со важечки индекс?",
    "website": "",
}


class ContactFormTests(TestCase):
    url = reverse("contact:contact")

    def test_page_renders(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_valid_submission_saves_and_redirects(self):
        resp = self.client.post(self.url, VALID_CONTACT)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(ContactMessage.objects.count(), 1)

        msg = ContactMessage.objects.get()
        self.assertEqual(msg.email, "ivana@example.com")
        self.assertFalse(msg.is_read)

    def test_valid_submission_notifies_staff(self):
        self.client.post(self.url, VALID_CONTACT)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Прашање за членство", mail.outbox[0].subject)

    def test_honeypot_blocks_bots(self):
        resp = self.client.post(self.url, {**VALID_CONTACT, "website": "http://spam.example"})

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_short_message_rejected(self):
        resp = self.client.post(self.url, {**VALID_CONTACT, "message": "здраво"})

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)
        self.assertContains(resp, "10", status_code=200)

    def test_invalid_email_rejected(self):
        self.client.post(self.url, {**VALID_CONTACT, "email": "not-an-email"})
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_htmx_submission_returns_success_partial_not_redirect(self):
        resp = self.client.post(self.url, VALID_CONTACT, headers={"hx-request": "true"})

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertTemplateUsed(resp, "contact/partials/_contact_success.html")

    def test_htmx_invalid_returns_422_with_form(self):
        resp = self.client.post(
            self.url, {**VALID_CONTACT, "email": ""}, headers={"hx-request": "true"}
        )

        self.assertEqual(resp.status_code, 422)
        self.assertTemplateUsed(resp, "contact/partials/_contact_form.html")

    def test_email_failure_does_not_break_the_page(self):
        with self.settings(EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend",
                           EMAIL_HOST="invalid.invalid", EMAIL_PORT=1):
            with self.assertLogs("contact.views", level="ERROR") as logs:
                resp = self.client.post(self.url, VALID_CONTACT)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertTrue(any("Failed to send" in line for line in logs.output))


class BookingFormTests(TestCase):
    url = reverse("contact:booking")

    def setUp(self):
        self.gym_class = GymClass.objects.create(
            title="HIIT", slug="hiit", short_desc="s", full_desc="f"
        )
        self.valid = {
            "name": "Стефан Ангеловски",
            "email": "stefan@example.com",
            "phone": "+389 71 987 654",
            "gym_class": self.gym_class.pk,
            "preferred_date": (timezone.localdate() + timedelta(days=3)).isoformat(),
            "preferred_time": "18:30",
            "notes": "",
            "website": "",
        }

    def test_page_renders(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_valid_booking_saves_as_pending(self):
        resp = self.client.post(self.url, self.valid)

        self.assertEqual(resp.status_code, 302)
        booking = Booking.objects.get()
        self.assertEqual(booking.status, Booking.PENDING)
        self.assertEqual(booking.gym_class, self.gym_class)

    def test_past_date_rejected(self):
        past = (timezone.localdate() - timedelta(days=1)).isoformat()
        resp = self.client.post(self.url, {**self.valid, "preferred_date": past})

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Booking.objects.count(), 0)

    def test_class_is_optional_for_a_free_trial(self):
        self.client.post(self.url, {**self.valid, "gym_class": ""})

        booking = Booking.objects.get()
        self.assertIsNone(booking.gym_class)

    def test_honeypot_blocks_bots(self):
        self.client.post(self.url, {**self.valid, "website": "spam"})
        self.assertEqual(Booking.objects.count(), 0)

    def test_inactive_classes_are_not_selectable(self):
        self.gym_class.is_active = False
        self.gym_class.save()

        resp = self.client.post(self.url, self.valid)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Booking.objects.count(), 0)
