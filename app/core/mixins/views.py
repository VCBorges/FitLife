from __future__ import annotations, unicode_literals

import json
import logging
import traceback
from typing import Any, TypeVar

from django.conf import settings
from django.http import HttpRequest, JsonResponse, QueryDict
from django.templatetags.static import static
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from app.core.exceptions import ProcessingError
from app.core.forms import BaseForm
from app.core.utils.forms import get_form_errors

if settings.DEBUG:
    from rich import print

BaseFormType = TypeVar('BaseFormType', bound=BaseForm)

logger = logging.getLogger(__name__)


class BaseTemplateViewMixin:
    template_name = 'core/_base.html'
    bundle: str
    title: str

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['bundle'] = static(f'bundles/{self.bundle}')
        context['images'] = {
            'fitlifeLogo': static('public/images/fitlife_logo.jpeg'),
        }
        return context

    def get(self, request: HttpRequest, *args, **kwargs) -> dict[str, Any]:
        return super().get(request, *args, **kwargs)


class BaseFormViewMixin:
    form_class: type[BaseFormType]
    valid_form_message: str = ''
    invalid_form_message: str = ''
    server_error_message: str = _(
        'There was an error processing your request. Please try again later.'
    )
    has_return_data: bool = False

    request: HttpRequest
    data: dict[str, Any] | QueryDict

    def parse_request_body(self, request: HttpRequest) -> dict[str, Any]:
        try:
            body = json.loads(request.body.decode('utf-8'))
            return body
        except Exception as e:
            raise ProcessingError(
                code=400,
                message='Invalid request body',
                params={'error': str(e)},
            )

    @staticmethod
    def get_response(
        status_code: int,
        message: str,
        data: dict = None,
        *args,
        **kwargs,
    ) -> dict[str, Any]:
        response = {
            'status_code': status_code,
            'message': message,
        }
        if data:
            response.update(data)
        return response

    def form_processing(
        self,
        form: BaseFormType,
        *args,
        **kwargs,
    ) -> dict[str, Any]:
        data = form.save()
        return data

    def get_form(self) -> BaseFormType:
        form = self.form_class(**self.get_form_kwargs())
        return form

    def get_form_kwargs(self, *args, **kwargs) -> dict[str, Any]:
        kwargs['data'] = self.data
        kwargs['files'] = self.request.FILES
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form: BaseFormType, *args, **kwargs) -> dict:
        if form.is_valid():
            data = self.form_processing(form)
            response = self.get_response(
                status_code=200,
                message=self.valid_form_message,
                data=data if self.has_return_data else None,
            )
            return response

    def form_invalid(self, form: BaseFormType, *args, **kwargs) -> dict[str, Any]:
        if not form.is_valid():
            errors = get_form_errors(form)
            response = self.get_response(
                status_code=400,
                message=self.invalid_form_message,
                data=errors,
            )
            return response

    def server_error(self, exception: dict, *args, **kwargs) -> dict[str, Any]:
        response = self.get_response(
            status_code=500,
            message=self.server_error_message,
            data=exception,  # TODO(Add traceback)
        )
        return response

    def get_body_data(self, request: HttpRequest) -> dict[str, Any] | QueryDict:
        if request.content_type == 'application/json':
            return self.parse_request_body(request)
        return getattr(request, request.method)

    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        return self.process_request(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        return self.process_request(request, *args, **kwargs)

    def process_request(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        self.request = request
        self.data = self.get_body_data(request)
        print(f'{self.data = }')
        try:
            form: BaseFormType = self.get_form()
            if form.is_valid():
                response = self.form_valid(form)
            else:
                response = self.form_invalid(form)
        except ProcessingError as error:  # TODO(Create a generic ValidationError)
            response = self.get_response(
                status_code=error.code,
                message=error.message,
                data=error.params,
            )
        except Exception as e:
            traceback.print_exc()
            response = self.server_error(exception={'error': str(e)})
        finally:
            print(f'{response = }')
            return JsonResponse(response, status=response['status_code'])


class BaseInstanceFormViewMixin(BaseFormViewMixin):
    def get_form_kwargs(self, *args, **kwargs) -> dict:
        kwargs['uuid'] = self.uuid
        return super.get_form_kwargs(self, *args, **kwargs)

    def post(
        self,
        request: HttpRequest,
        *args,
        **kwargs,
    ) -> JsonResponse:
        self.uuid = kwargs.get('uuid')
        return super().post(request, *args, **kwargs)

    def get(
        self,
        request: HttpRequest,
        *args,
        **kwargs,
    ) -> JsonResponse:
        self.uuid = kwargs.get('uuid')
        return super().get(request, *args, **kwargs)


class CsrfExemptMixin:
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
