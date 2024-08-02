from django.contrib import admin
from django.urls import include, path

from src.gym.views import CreateListWorkoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__reload__/', include('django_browser_reload.urls')),
    # path('accounts/', include('allauth.urls')),
    path('', include('src.users.urls')),
    path('testing/', CreateListWorkoutView.as_view(), name='testing'),
]
