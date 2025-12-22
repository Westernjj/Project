from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views as auth_views

# ↓↓↓ ДОДАЄМО ІМПОРТИ ДЛЯ JWT ↓↓↓
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('accounts.urls')),
    
    path('shop/', include('shop.urls')),
    path('shop2/', include('shop2.urls')),
    path('', include('shop.urls')),

    path('api/', include('api.urls')),
    
    # Старий вхід по токену
    path('api-token-auth/', auth_views.obtain_auth_token),

    # Отримати токен 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Оновити токен 
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)