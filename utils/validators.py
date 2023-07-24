import re
from django.core.exceptions import ValidationError


def rut_validator(value):
    rut_pattern = r"^\d{8}-[0-9a-zA-Z]$"
    if not re.match(rut_pattern, value):
        raise ValidationError(
            "Rut invalid, format required is: XXXXXXX-Y check: https://es.wikipedia.org/wiki/Rol_%C3%9Anico_Tributario"
        )
