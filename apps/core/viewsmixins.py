from __future__ import annotations, unicode_literals

import json
import logging
import traceback
from typing import Any, Literal, Mapping, override

from django.conf import settings
from django.db.models.query import QuerySet
from django.http import HttpRequest, JsonResponse
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_exempt

from apps.core.constants import Language
from apps.core.exceptions import BaseAPIError
from apps.core.typed import BaseFormType, DjangoModelType
from apps.core.utils import get_or_404

logger = logging.getLogger(__name__)

HTTPMethods = list[Literal['post', 'get', 'put', 'delete']]

ResponseClass = JsonResponse | TemplateResponse


class BaseView:
    def __init__(self):
        super().__init__()
        self.language = Language[get_language().upper()]


class BaseTemplateContextMixin(BaseView):
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({'LANGUAGES': settings.LANGUAGES})
        return context


class BaseAPIView(BaseView):
    http_method_names: HTTPMethods = []
    request: HttpRequest
    model: type[DjangoModelType] | None = None
    queryset: QuerySet[DjangoModelType] | None = None
    object: DjangoModelType | None = None
    data: Mapping[str, Any]
    pk_url_kwarg = 'pk'
    kwargs: dict[str, Any]
    template_engine: str = 'django'

    def _parse_json(self) -> dict[str, Any]:
        if self.request.body == b'':
            return {}
        try:
            print(f'{self.request.body = }')
            parsed = json.loads(self.request.body.decode('utf-8'))
            return parsed
        except json.JSONDecodeError as error:
            traceback.print_exc()
            raise BaseAPIError(
                status_code=400,
                data={'error': str(error)},
            )

    def get_form(self, form_class: type[BaseFormType]) -> BaseFormType:
        form = form_class(**self.get_form_kwargs())
        return form

    def get_form_kwargs(self, *args, **kwargs) -> dict[str, Any]:
        kwargs['data'] = self.data
        kwargs['files'] = self.request.FILES
        kwargs['request'] = self.request
        if self.object:
            kwargs['instance'] = self.object
        return kwargs

    def get_cleaned_data(self, form_class: type[BaseFormType]) -> dict[str, Any]:
        form: BaseFormType = self.get_form(form_class)
        form.is_valid()
        return form.cleaned_data

    def _set_request_data(self) -> None:
        # print(f'{self.request.POST = }')
        # print(f'{self.request.content_type = }')
        # print(f'{self.request.method = }')
        if self.request.content_type != 'application/json' and self.request.method in [
            'GET',
            'POST',
        ]:
            data = getattr(self.request, self.request.method)
        else:
            data = self._parse_json()
        self.data = data

    @override
    def get_object(self) -> DjangoModelType | None:
        if self.queryset or self.model:
            return get_or_404(
                self.queryset or self.model,
                pk=self.kwargs.get(self.pk_url_kwarg),
            )

        return None

    @override
    def setup(self, request: HttpRequest, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self._set_request_data()
        self.object = self.get_object()

    @override
    def dispatch(self, *args: Any, **kwargs: Any) -> JsonResponse:
        try:
            response = super().dispatch(*args, **kwargs)
        except Exception as error:
            traceback.print_exc()
            response = self.handle_exception(error)
        return response

    def handle_exception(self, exception: Exception) -> JsonResponse:
        if isinstance(exception, BaseAPIError):
            return self.render_to_json(
                status_code=exception.status_code,
                data={
                    'errors': exception.error_dict,
                },
            )
        return self.render_to_json(status_code=500)

    def render_to_json(
        self,
        *,
        data: dict[str, Any] | None = None,
        status_code: int = 200,
    ) -> JsonResponse:
        if data is None:
            data = {}
        return JsonResponse(
            data=data,
            status=status_code,
            json_dumps_params={'ensure_ascii': False},
        )

    def render_to_template(
        self,
        template: str,
        context: dict[str, Any] | None = None,
        status_code: int = 200,
        **response_kwargs,
    ) -> TemplateResponse:
        if context is None:
            context = {}
        response_kwargs.setdefault('content_type', self.request.content_type)
        return TemplateResponse(
            request=self.request,
            status=status_code,
            template=template,
            context=self.get_context_data(**context),
            using=self.template_engine,
            **response_kwargs,
        )

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        kwargs.setdefault('view', self)
        return kwargs

    def post(self, *args, **kwargs) -> ResponseClass:
        raise NotImplementedError

    def get(self, *args, **kwargs) -> ResponseClass:
        raise NotImplementedError

    def put(self, *args, **kwargs) -> ResponseClass:
        raise NotImplementedError

    def delete(self, *args, **kwargs) -> ResponseClass:
        raise NotImplementedError


class CsrfExemptMixin:
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
