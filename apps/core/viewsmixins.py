from __future__ import annotations, unicode_literals

import json
import logging
from typing import Any, Literal, Mapping, override

from django.db.models.query import QuerySet

# from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from apps.core.exceptions import BaseAPIError
from apps.core.typed import BaseFormType, DjangoModelType
from apps.core.utils import get_or_404

logger = logging.getLogger(__name__)

HTTPMethods = list[Literal['post', 'get', 'put', 'delete']]

ResponseClass = JsonResponse | TemplateResponse


class BaseTemplateContextMixin:
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context


class BaseAPIView:
    http_method_names: HTTPMethods = []
    request: HttpRequest
    model: type[DjangoModelType] | None = None
    queryset: QuerySet[DjangoModelType] | None = None
    object: DjangoModelType | None = None
    data: Mapping[str, Any]
    pk_url_kwarg = 'pk'
    kwargs: dict[str, Any]

    def _parse_json(self, request: HttpRequest) -> dict[str, Any]:
        try:
            parsed = json.loads(request.body.decode('utf-8'))
            return parsed
        except json.JSONDecodeError as error:
            raise BaseAPIError(
                code=400,
                message='Invalid request body',
                params={'error': str(error)},
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

    def _set_request_data(self) -> Mapping[str, Any]:
        if (
            self.request.content_type == 'application/json'
            and self.request.method not in ['GET', 'HEAD']
        ):
            data = self._parse_json(self.request)
        else:
            data = getattr(self.request, self.request.method)
        self.data = data

    @override
    def get_object(self) -> DjangoModelType | None:
        if self.queryset:
            return get_or_404(
                model_or_queryset=self.queryset,
                pk=self.kwargs.get(self.pk_url_kwarg),
            )

        if self.model:
            return get_or_404(
                model_or_queryset=self.model,
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
        return JsonResponse(
            data=data,
            status=status_code,
        )

    def render_to_template(
        self,
        template: str,
        context: dict[str, Any],
        **response_kwargs,
    ) -> TemplateResponse:
        response_kwargs.setdefault('content_type', self.content_type)
        return TemplateResponse(
            request=self.request,
            template=template,
            context=self.get_context_data(**context),
            using=self.template_engine,
            **response_kwargs,
        )

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        kwargs.setdefault('view', self)
        if self.extra_context is not None:
            kwargs.update(self.extra_context)
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
