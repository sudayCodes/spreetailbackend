from django.contrib import admin
from .models import Settlement


@admin.register(Settlement)
class SettlementAdmin(admin.ModelAdmin):
    list_display = ['payer', 'receiver', 'amount', 'group', 'created_at']
    list_filter = ['group']
