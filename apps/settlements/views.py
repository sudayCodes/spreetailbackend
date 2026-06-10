from rest_framework import viewsets, mixins
from django_filters.rest_framework import DjangoFilterBackend
from .models import Settlement
from .serializers import SettlementSerializer, SettlementCreateSerializer


class SettlementViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group', 'payer', 'receiver']

    def get_queryset(self):
        return Settlement.objects.filter(
            group__members__user=self.request.user
        ).select_related('payer', 'receiver', 'group')

    def get_serializer_class(self):
        if self.action == 'create':
            return SettlementCreateSerializer
        return SettlementSerializer
