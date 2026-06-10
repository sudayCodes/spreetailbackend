from rest_framework import serializers
from apps.accounts.serializers import UserSerializer
from .models import Group, GroupMember


class GroupMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = GroupMember
        fields = ['user', 'joined_at']


class GroupSerializer(serializers.ModelSerializer):
    members = GroupMemberSerializer(many=True, read_only=True)
    member_count = serializers.IntegerField(source='members.count', read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'type', 'invite_token', 'created_at', 'member_count', 'members']
        read_only_fields = ['id', 'invite_token', 'created_at']


class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name', 'type']

    def create(self, validated_data):
        group = Group.objects.create(**validated_data)
        GroupMember.objects.create(group=group, user=self.context['request'].user)
        return group
