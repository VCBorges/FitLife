from django.urls import path

from app.users import views

urlpatterns = [
    path(
        'me/',
        views.UserTemplateView.as_view(),
        name='user_template',
    ),
    path(
        'register/',
        views.RegisterTemplateView.as_view(),
        name='user_register_template',
    ),
    path(
        'registration/',
        views.UserRegisterView.as_view(),
        name='user_register',  
    )
]
