from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from news import settings

urlpatterns = [
    path('admin/', admin.site.urls),

] + i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('news_app.urls')),
    path('user/', include('user.urls')),
    path('main/', include('main.urls'))
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.ADMIN_MEDIA_PREFIX, document_root=settings.ADMIN_MEDIA_PREFIX)