from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.core.urls')),
    path('users/', include('app.users.urls')),
    path('gym/', include('app.gym.urls')),
]
