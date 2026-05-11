from django.core import mail
from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APIClient


class EmailTaskViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_email_requires_valid_payload(self):
        response = self.client.post("/api/email/", {"email": "not-email"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertIn("content", response.data)

    @override_settings(
        CELERY_TASK_ALWAYS_EAGER=True,
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        EMAIL_HOST_USER="sender@example.com",
        EMAIL_HOST_PASSWORD="test-password",
        DEFAULT_FROM_EMAIL="sender@example.com",
    )
    def test_email_task_sends_email_when_configured(self):
        response = self.client.post(
            "/api/email/",
            {
                "email": "recipient@example.com",
                "subject": "Hello",
                "content": "This is the email body.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["recipient@example.com"])
        self.assertEqual(mail.outbox[0].subject, "Hello")
        self.assertEqual(mail.outbox[0].body, "This is the email body.")
