from __future__ import annotations, unicode_literals

import json
import logging
import traceback
from typing import Any, Literal, override

# from django.conf import settings
from django.forms.utils import ErrorDict
from django.http import HttpRequest, JsonResponse, QueryDict
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from src.core.exceptions import ProcessingError
from src.core.querysets import get_or_404
from src.core.typed import BaseFormType, ModelType

logger = logging.getLogger(__name__)

HTTPMethods = list[Literal['post', 'get', 'put', 'delete']]


class BaseTemplateViewContextMixin:
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context


class BaseFormViewMixin:
    http_method_names: HTTPMethods = []
    form_class: type[BaseFormType]
    valid_form_message: str = ''
    invalid_form_message: str = _('Invalid data')
    server_error_message: str = _(
        'There was an error processing your request. Please try again later.'
    )
    request: HttpRequest
    model: type[ModelType] | None = None
    data: dict[str, Any] | QueryDict
    pk_url_kwarg = 'pk'
    object: ModelType | None

    def parse_request_body(self, request: HttpRequest) -> dict[str, Any]:
        try:
            body = json.loads(request.body.decode('utf-8'))
            return body
        except json.JSONDecodeError as error:
            raise ProcessingError(
                code=400,
                message='Invalid request body',
                params={'error': str(error)},
            )

    def get_response(
        self,
        status_code: int,
        message: str | None = None,
        data: dict[str, Any] | None = None,
        *args,
        **kwargs,
    ) -> dict[str, Any]:
        response = {
            'status_code': status_code,
            'data': {
                'message': _(message),
            },
        }
        if data:
            response['data'].update(data)
        return response

    def get_form(self, form_class: type[BaseFormType]) -> BaseFormType:
        form = form_class(**self.get_form_kwargs())
        return form

    def get_cleaned_data(self, form_class: type[BaseFormType]) -> dict[str, Any]:
        form: BaseFormType = self.get_form(form_class)
        form.is_valid()
        return form.cleaned_data

    def get_form_kwargs(self, *args, **kwargs) -> dict[str, Any]:
        kwargs['data'] = self.data
        kwargs['files'] = self.request.FILES
        kwargs['request'] = self.request
        if self.object:
            kwargs['instance'] = self.object
        return kwargs

    def form_valid(self, form: BaseFormType, *args, **kwargs) -> dict[str, Any]:
        if form.is_valid():
            data = self.process(form)
            response = self.get_response(
                status_code=200,
                message=self.valid_form_message,
                data=data,
            )
            return response

    def form_invalid(self, form: BaseFormType, *args, **kwargs) -> dict[str, Any]:
        errors = self.get_form_errors(form)
        response = self.get_response(
            status_code=400,
            message=self.invalid_form_message,
            data=errors,
        )
        return response

    def get_form_errors(self, form: BaseFormType) -> ErrorDict:
        return {'errors': form.errors}

    def server_error(self, exception: dict, *args, **kwargs) -> dict[str, Any]:
        response = self.get_response(
            status_code=500,
            message=self.server_error_message,
            data=exception,  # TODO(Add traceback)
        )
        return response

    def get_data(self) -> dict[str, Any] | QueryDict:
        if self.request.content_type == 'application/json':
            return self.parse_request_body(self.request)

        return getattr(self.request, self.request.method)

    @override
    def get_object(self) -> ModelType | None:
        if self.model:
            return get_or_404(
                model=self.model,
                pk=self.kwargs.get(self.pk_url_kwarg),
            )
        return None

    @override
    def setup(self, request: HttpRequest, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.data = self.get_data()
        self.object = self.get_object()

    @override
    def dispatch(self, *args: Any, **kwargs: Any) -> JsonResponse:
        try:
            data = super().dispatch(*args, **kwargs)
            response = self.get_response(
                status_code=200,
                message=self.valid_form_message,
                data=data,
            )
        except ProcessingError as error:
            response = self.get_response(
                status_code=error.code,
                message=error.message,
                data=error.params,
            )
        except Exception as e:
            traceback.print_exc()
            response = self.server_error(exception={'error': str(e)})
        finally:
            return JsonResponse(
                data=response['data'],
                status=response['status_code'],
            )


class CsrfExemptMixin:
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
