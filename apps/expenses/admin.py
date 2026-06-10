from django.contrib import admin
from .models import Expense, ExpenseSplit


class ExpenseSplitInline(admin.TabularInline):
    model = ExpenseSplit
    extra = 0


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['description', 'group', 'paid_by', 'total_amount', 'split_type', 'category', 'created_at']
    list_filter = ['split_type', 'category']
    inlines = [ExpenseSplitInline]
