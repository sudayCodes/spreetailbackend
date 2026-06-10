from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.request import Request


# ── Utility functions ──────────────────────────────────────────────────────────

def is_authenticated(request: Request) -> bool:
    """Return True if the request carries a valid JWT and an active user."""
    return request.user is not None and request.user.is_authenticated


def get_current_user(request: Request):
    """Return the authenticated user, or None."""
    return request.user if is_authenticated(request) else None


def user_from_token(token: str):
    """
    Resolve a raw JWT string to a User instance without going through a view.
    Useful in WebSocket handshakes or background tasks.
    Returns None if the token is invalid or expired.
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()
    try:
        validated = AccessToken(token)
        return User.objects.get(id=validated['user_id'])
    except (TokenError, User.DoesNotExist):
        return None


# ── Permission classes ─────────────────────────────────────────────────────────

class IsGroupMember(BasePermission):
    """
    Allow access only if the authenticated user is a member of the group
    identified by `group_pk` in the URL kwargs.
    """
    message = 'You are not a member of this group.'

    def has_permission(self, request, view):
        if not is_authenticated(request):
            return False
        group_pk = view.kwargs.get('group_pk') or view.kwargs.get('pk')
        if not group_pk:
            return True
        from apps.groups.models import GroupMember
        return GroupMember.objects.filter(group_id=group_pk, user=request.user).exists()


class IsOwnerOrReadOnly(BasePermission):
    """
    Full access to the object owner; read-only to other authenticated users.
    The model must have a `user` or `paid_by` field pointing to the owner.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        owner = getattr(obj, 'user', None) or getattr(obj, 'paid_by', None)
        return owner == request.user


# ── Custom JWT token view (returns user data with tokens) ─────────────────────

class TokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': str(self.user.id),
            'email': self.user.email,
            'name': self.user.name,
        }
        return data


class LoginView(TokenObtainPairView):
    """
    POST /api/auth/login/
    Returns access + refresh tokens alongside basic user info.
    """
    serializer_class = TokenSerializer
