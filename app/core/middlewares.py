from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class NoCacheStaticFilesMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.path.startswith(
            '/static/'
        ):  # Adjust the path according to your static files URL
            response['Cache-Control'] = 'no-store'
        return response


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        exempt_urls = [
            reverse('user_register_template'),
            reverse('login_template'),
        ]

        if not request.user.is_authenticated and request.path not in exempt_urls:
            return redirect('login_template')  # Redirect to your login page

        response = self.get_response(request)
        return response
