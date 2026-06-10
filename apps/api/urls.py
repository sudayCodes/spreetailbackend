from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .auth import LoginView

# All /api/* routes live here. config/urls.py just delegates to this file.

auth_patterns = [
    path('login/', LoginView.as_view(), name='auth_login'),
    path('refresh/', TokenRefreshView.as_view(), name='auth_refresh'),
]

urlpatterns = [
    # Auth
    path('auth/', include(auth_patterns)),

    # Resources
    path('accounts/', include('apps.accounts.urls')),
    path('groups/', include('apps.groups.urls')),
    path('expenses/', include('apps.expenses.urls')),
    path('settlements/', include('apps.settlements.urls')),
    path('chat/', include('apps.chat.urls')),

    # Docs
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
]
