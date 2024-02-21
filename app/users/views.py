from typing import Any

from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from ..core.views import BaseTemplateView, LoggedOutFormView, LoggedOutTemplateView
from . import forms


class LoginTemplateView(LoggedOutTemplateView):
    template_name = 'core/login.html'
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['endpoints'] = {
            'login': reverse('login'),
        }
        return context

class UserTemplateView(BaseTemplateView):
    template_name = 'users/user.html'
    


class RegisterTemplateView(LoggedOutTemplateView):
    template_name = 'users/user_registration.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['endpoints'] = {
            'register': reverse('user_register'),
        }
        return context

class LogoutView(BaseLogoutView):
    next_page = reverse_lazy('login_template')


class LoginView(
    LoggedOutFormView,
    BaseLoginView,
):
    form_class = AuthenticationForm
    success_url = reverse_lazy('login')
    success_message = 'You are now logged in.'
    has_return_data = True

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()  # FIXME:(set success_url to home)
            if redirect_to == self.request.path:
                raise ValueError(
                    'Redirection loop for authenticated user detected. Check that '
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def form_processing(
        self, form: AuthenticationForm, *args, **kwargs
    ) -> dict[str, Any]:
        user = form.get_user()
        # if user.is_staff:
        #     raise ValidationError('Internal error.')
        login(self.request, form.get_user())
        return {
            'redirect_url': reverse('user_template'),
        }


class UserRegisterView(LoggedOutFormView):
    form_class = forms.UserRegisterForm
    has_return_data = True
    
    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        print(f'{request.POST = }')
        return super().post(request, *args, **kwargs)
