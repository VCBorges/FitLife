from django.urls import path

from apps.users import views

templates_urls = [
    path('login/', views.UserLoginTemplateView.as_view(), name='login_template'),
    path('signup/', views.UserSignUpTemplateView.as_view(), name='signup_template'),
]

api_urls = [
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('login/submit/', views.UserLoginView.as_view(), name='login'),
    path('signup/submit/', views.UserSignUpView.as_view(), name='signup'),
]

urlpatterns = templates_urls + api_urls
