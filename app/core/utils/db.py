from django import forms

from app.core.types import CreateDTOType, ModelType, UpdateDTOType


# TODO: Add type hints in DTO
def create(
    *,
    model: type[ModelType],
    dto: CreateDTOType,
    commit: bool = True,
    **fields,
) -> ModelType:
    instance = model(
        **dto.to_dict(),
        **fields,
    )
    if commit:
        instance.save()
    return instance


def update(
    dto: UpdateDTOType,
    *,
    commit: bool = True,
) -> ModelType:
    for field, value in dto.to_dict().items():
        setattr(dto.instance, field, value)
    print(f'{dto.instance = }')
    if commit:
        dto.instance.save()
    return dto.instance


def get_by_id(
    model: type[ModelType],
    id: int,
) -> ModelType:
    return model.objects.get(pk=id)


def get_by_uuid(
    model: type[ModelType],
    uuid: str,
    **lookup_filters,
) -> ModelType:
    return model.objects.get(uuid=uuid, **lookup_filters)


# TODO: Add support to use filtering lookups
def get_by_uuid_or_400(
    model: type[ModelType],
    uuid: str,
    message: str = 'Instance not found',
    status_code: int = 400,
) -> ModelType:
    try:
        return get_by_uuid(model, uuid)
    except model.DoesNotExist:
        raise forms.ValidationError(message)


def bulk_create(
    *,
    model: type[ModelType],
    dtos,
    **fields,
) -> list[ModelType]:
    instances = [
        create(
            model=model,
            dto=dto,
            commit=False,
            **fields,
        )
        for dto in dtos
    ]
    return model.objects.bulk_create(instances)


def bulk_update(
    *,
    model: type[ModelType],
    dtos: list,
) -> None:
    instances = [update(dto=dto, commit=False) for dto in dtos]
    model.objects.bulk_update(
        instances,
        fields=dtos[0].get_field_names(),
    )


def bulk_delete(
    *,
    model: type[ModelType],
    instances: list[ModelType],
    **lookup_filters,
) -> None:
    queryset = model.objects.filter(
        uuid__in=[instance.uuid for instance in instances],
        **lookup_filters,
    )
    queryset.delete()
