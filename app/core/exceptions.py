from django.forms import ValidationError


class ProcessingError(ValidationError):
    pass
