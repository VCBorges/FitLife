from django.utils.deprecation import MiddlewareMixin


class NoCacheStaticFilesMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.path.startswith(
            '/static/'
        ):  # Adjust the path according to your static files URL
            response['Cache-Control'] = 'no-store'
        return response
