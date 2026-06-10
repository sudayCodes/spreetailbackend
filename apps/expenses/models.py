import uuid
from django.conf import settings
from django.db import models


class Expense(models.Model):
    SPLIT_EQUAL = 'equal'
    SPLIT_UNEQUAL = 'unequal'
    SPLIT_PERCENTAGE = 'percentage'
    SPLIT_SHARE = 'share'
    SPLIT_CHOICES = [
        (SPLIT_EQUAL, 'Equal'),
        (SPLIT_UNEQUAL, 'Unequal'),
        (SPLIT_PERCENTAGE, 'Percentage'),
        (SPLIT_SHARE, 'Share'),
    ]

    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('travel', 'Travel'),
        ('hotel', 'Hotel'),
        ('entertainment', 'Entertainment'),
        ('other', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey('groups.Group', on_delete=models.CASCADE, related_name='expenses')
    paid_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='paid_expenses')
    description = models.TextField()
    # stored as integer cents — $10.50 → 1050
    total_amount = models.PositiveIntegerField()
    split_type = models.CharField(max_length=20, choices=SPLIT_CHOICES, default=SPLIT_EQUAL)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='updated_expenses'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.description} (${self.total_amount / 100:.2f})'


class ExpenseSplit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='splits')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='expense_splits')
    # stored as integer cents
    amount_owed = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.user} owes ${self.amount_owed / 100:.2f} for {self.expense}'
