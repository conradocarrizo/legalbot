from django.db import IntegrityError
from django.forms import ValidationError
import pytest
from societies.models import Rut


UNIQUE_KEY_CONSTRAINT = "societies_rut_code_key"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "name, code, expected_error",
    [
        ("Juan Lopez", "12345678-K", False),
        ("Armando Paredes", "21045678--", True),
        ("Maria Bravo", "22345678-2", False),
        ("Julieta Barrera", "2232567812", True),
    ],
)
def test_rut_creation_code_validator(name, code, expected_error):
    rut = Rut(name=name, code=code)

    try:
        rut.full_clean()
        rut.save()

        assert not expected_error

    except ValidationError:
        assert expected_error


@pytest.mark.django_db
def test_unique_constraint_rut_code():
    rut_1 = {
        "name": "Pepito S.A.",
        "code": "87325618-2",
    }
    rut_2 = {
        "name": "Maria Ceballos",
        "code": "87325618-2",
    }

    with pytest.raises(IntegrityError) as exc:
        for rut in [rut_1, rut_2]:
            Rut.objects.create(**rut)
    assert UNIQUE_KEY_CONSTRAINT in str(exc.value)
