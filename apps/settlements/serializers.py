from rest_framework import serializers
from apps.accounts.serializers import UserSerializer
from .models import Settlement


class SettlementSerializer(serializers.ModelSerializer):
    payer = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = Settlement
        fields = ['id', 'group', 'payer', 'receiver', 'amount', 'created_at']
        read_only_fields = ['id', 'created_at']


class SettlementCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settlement
        fields = ['group', 'receiver', 'amount']

    def create(self, validated_data):
        return Settlement.objects.create(payer=self.context['request'].user, **validated_data)
