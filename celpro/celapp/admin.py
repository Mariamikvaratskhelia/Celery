from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("email_address", "text", "created_at")
    search_fields = ("email_address", "text")
