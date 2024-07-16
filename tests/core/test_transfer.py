from app.core import transfer


def test_update_dto_to_dict_to_not_have_instance_field():
    instance = object()
    dto = transfer.UpdateDTO(instance=instance)

    result = dto.to_dict()

    assert 'instance' not in result


def test_update_dto_get_field_names_to_not_have_instance_field():
    result = transfer.UpdateDTO.get_field_names()

    assert 'instance' not in result
