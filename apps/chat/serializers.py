from rest_framework import serializers
from apps.accounts.serializers import UserSerializer
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'group', 'sender', 'content', 'created_at']
        read_only_fields = ['id', 'sender', 'created_at']


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['group', 'content']

    def create(self, validated_data):
        return Message.objects.create(sender=self.context['request'].user, **validated_data)
