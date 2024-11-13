from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.users.urls')),
    path('', include('apps.gym.urls')),
]


if settings.DEBUG:
    urlpatterns.extend(
        [
            path('__reload__/', include('django_browser_reload.urls')),
        ]
    )
