from datetime import datetime

from django.core.exceptions import ValidationError


def year_validate(value):
    if value > datetime.now().year:
        raise ValidationError(f'{value} is not a correct year!')
