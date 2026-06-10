from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Expense
from .serializers import ExpenseSerializer, ExpenseCreateSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group', 'paid_by', 'category', 'split_type']

    def get_queryset(self):
        return Expense.objects.filter(
            group__members__user=self.request.user
        ).select_related('paid_by', 'updated_by').prefetch_related('splits__user')

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return ExpenseCreateSerializer
        return ExpenseSerializer
