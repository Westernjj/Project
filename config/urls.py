# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('accounts.urls')),  # ← тільки тут

    path('shop/', include('shop.urls')),
    path('shop2/', include('shop2.urls')),
    path('', include('shop.urls')),  # головна з shop
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
