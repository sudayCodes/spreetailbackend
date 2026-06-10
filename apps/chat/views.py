from rest_framework import viewsets, mixins
from django_filters.rest_framework import DjangoFilterBackend
from .models import Message
from .serializers import MessageSerializer, MessageCreateSerializer


class MessageViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group']

    def get_queryset(self):
        return Message.objects.filter(
            group__members__user=self.request.user
        ).select_related('sender')

    def get_serializer_class(self):
        if self.action == 'create':
            return MessageCreateSerializer
        return MessageSerializer
