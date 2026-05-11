from rest_framework import serializers

from .models import Message


class DelayTaskSerializer(serializers.Serializer):
    text = serializers.CharField()


class EmailTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("id", "email_address", "text", "created_at")
        read_only_fields = ("id", "created_at")
