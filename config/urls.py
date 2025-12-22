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

    # === ТИМЧАСОВИЙ КОД: СТВОРЕННЯ АДМІНА ===
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        print("Creating superuser...")
        User.objects.create_superuser('admin', 'admin@example.com', 'admin12345')
        print("SUPERUSER CREATED: admin / admin12345")
    else:
        print("Superuser already exists")
except Exception as e:
    print(f"Error creating superuser: {e}")
# ========================================