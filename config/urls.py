from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/', include('shop.urls')),   # підключає маршрути з програми shop
    path('shop2/', include('shop2.urls')), # якщо є друга програма
    path('', include('shop.urls')),        # головна сторінка бере маршрути з shop
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
