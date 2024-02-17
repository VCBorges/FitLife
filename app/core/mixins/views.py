from __future__ import unicode_literals

import json
import traceback
from typing import Any, TypeVar

from django.http import HttpRequest, JsonResponse, QueryDict
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from rich import print

from ..exceptions import ProcessingError
from ..forms import BaseForm
from ..utils.forms import get_form_errors

T = TypeVar('T', bound=BaseForm)


class BaseContextTemplateViewMixin:
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request: HttpRequest, *args, **kwargs) -> dict[str, Any]:
        return super().get(request, *args, **kwargs)


class BaseFormViewMixin:
    form_class: type[T] = None
    form_valid_message: str = None
    form_invalid_message: str = None
    server_error_message: str = _(
        'There was an error processing your request. Please try again later.'
    )
    has_return_data: bool = False

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
        form: T,
        *args,
        **kwargs,
    ) -> dict[str, Any]:
        data = form.save()
        return data

    def get_form(self, *args, **kwargs) -> T:
        form = self.form_class(**self.get_form_kwargs())
        return form

    def get_form_kwargs(self, *args, **kwargs) -> dict[str, Any]:
        # kwargs['data'] = self.request.POST
        kwargs['data'] = self.data
        kwargs['files'] = self.request.FILES
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form: T, *args, **kwargs) -> dict:
        if form.is_valid():
            data = self.form_processing(form)
            response = self.get_response(
                status_code=200,
                message=self.form_valid_message,
                data=data if self.has_return_data else None,
            )
            return response

    def form_invalid(self, form: T, *args, **kwargs) -> dict[str, Any]:
        if not form.is_valid():
            errors = get_form_errors(form)
            response = self.get_response(
                status_code=400,
                message=self.form_invalid_message,
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
        return request.POST

    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        self.request = request
        self.data = self.get_body_data(request)
        try:
            form: T = self.get_form()
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


class BaseUpdateFormViewMixin:
    def get_form_kwargs(self, *args, **kwargs) -> dict:
        kwargs['pk'] = self.pk
        return super.get_form_kwargs(self, *args, **kwargs)

    def post(self, request: HttpRequest, pk, *args, **kwargs):
        self.pk = pk
        return self.post(request, pk, *args, **kwargs)


class CsrfExemptMixin:
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
