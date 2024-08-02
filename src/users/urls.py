from django.urls import path

from src.users import views

urlpatterns = [
    path('login/', views.UserLoginTemplateView.as_view(), name='login_template'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('authenticate/', views.UserLoginView.as_view(), name='authenticate'),
    path('signup/', views.UserSignUpView.as_view(), name='signup'),
]
