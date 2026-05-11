from django.db import models


class Message(models.Model):
    email_address = models.EmailField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email_address}: {self.text[:30]}"
