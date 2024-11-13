from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('apps.users.urls')),
    path('', include('apps.gym.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
)


if settings.DEBUG:
    urlpatterns.extend(
        [
            path('__reload__/', include('django_browser_reload.urls')),
        ]
    )
