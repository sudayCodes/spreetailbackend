from rest_framework import serializers
from .models import Expense, ExpenseSplit


class ExpenseSplitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseSplit
        fields = ['id', 'user', 'amount_owed']


class ExpenseSerializer(serializers.ModelSerializer):
    splits = ExpenseSplitSerializer(many=True, read_only=True)

    class Meta:
        model = Expense
        fields = [
            'id', 'group', 'paid_by', 'description', 'total_amount',
            'split_type', 'category', 'created_at', 'updated_at', 'updated_by', 'splits',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'updated_by']


class ExpenseCreateSerializer(serializers.ModelSerializer):
    splits = ExpenseSplitSerializer(many=True)

    class Meta:
        model = Expense
        fields = ['group', 'paid_by', 'description', 'total_amount', 'split_type', 'category', 'splits']

    def create(self, validated_data):
        splits_data = validated_data.pop('splits')
        expense = Expense.objects.create(**validated_data)
        ExpenseSplit.objects.bulk_create([
            ExpenseSplit(expense=expense, **s) for s in splits_data
        ])
        return expense

    def update(self, instance, validated_data):
        splits_data = validated_data.pop('splits', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.updated_by = self.context['request'].user
        instance.save()
        if splits_data is not None:
            instance.splits.all().delete()
            ExpenseSplit.objects.bulk_create([
                ExpenseSplit(expense=instance, **s) for s in splits_data
            ])
        return instance
