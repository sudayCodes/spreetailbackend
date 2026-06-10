from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Group, GroupMember
from .serializers import GroupSerializer, GroupCreateSerializer


class GroupViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Group.objects.filter(members__user=self.request.user).prefetch_related('members__user')

    def get_serializer_class(self):
        if self.action == 'create':
            return GroupCreateSerializer
        return GroupSerializer

    @action(detail=False, methods=['get'], url_path='join/(?P<token>[^/.]+)')
    def join_by_token(self, request, token=None):
        group = get_object_or_404(Group, invite_token=token)
        _, created = GroupMember.objects.get_or_create(group=group, user=request.user)
        return Response(GroupSerializer(group, context={'request': request}).data,
                        status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], url_path='leave')
    def leave(self, request, pk=None):
        group = self.get_object()
        GroupMember.objects.filter(group=group, user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['delete'], url_path='members/(?P<user_id>[^/.]+)')
    def remove_member(self, request, pk=None, user_id=None):
        group = self.get_object()
        GroupMember.objects.filter(group=group, user_id=user_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
