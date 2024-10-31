from django.urls import path

from apps.users import views

templates_urls = [
    path('login/', views.UserLoginTemplateView.as_view(), name='login_template'),
    path('signup/', views.UserSignUpTemplateView.as_view(), name='signup_template'),
    path('profile/', views.UserProfileTemplateView.as_view(), name='profile_template'),
]

api_urls = [
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('session/', views.UserLoginView.as_view(), name='login'),
    path('create-account/', views.UserSignUpView.as_view(), name='signup'),
    path('update-user/', views.UpdateUserView.as_view(), name='update_user'),
]

urlpatterns = templates_urls + api_urls
