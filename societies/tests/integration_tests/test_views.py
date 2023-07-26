from urllib.parse import urlencode
import pytest
from django.urls import reverse
from societies.models import Society, Rut


@pytest.mark.django_db
def test_retrieve_society(authenticated_api_client):
    rut = Rut.objects.create(
        code="12345678-9",
        name="Nombre de la sociedad",
    )
    society = Society.objects.create(
        rut=rut,
        actions=1000,
    )

    url = reverse("society-detail", args=[society.pk])

    response = authenticated_api_client.get(url)

    assert response.status_code == 200

    assert response.data["rut"]["code"] == "12345678-9"
    assert response.data["rut"]["name"] == "Nombre de la sociedad"
    assert response.data["actions"] == 1000


@pytest.mark.django_db
def test_create_society_member(authenticated_api_client):
    rut = Rut.objects.create(
        code="12345678-9",
        name="Nombre de la sociedad",
    )
    society = Society.objects.create(
        rut=rut,
        actions=1000,
    )
    url = reverse("society-create-member", kwargs={"pk": society.id})

    data = {
        "rut": {"code": "12212118-c", "name": "Juan Carlos"},
        "address": "Avenida Siempre Viva 2132",
        "actions": 1200,
    }

    response = authenticated_api_client.post(url, data=data, format="json")
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_society_admin(authenticated_api_client):
    rut = Rut.objects.create(
        code="12345678-9",
        name="Nombre de la sociedad",
    )
    society = Society.objects.create(
        rut=rut,
        actions=1000,
    )
    url = reverse("society-create-admin", kwargs={"pk": society.id})

    data = {
        "rut": {"code": "12345678-2", "name": "Maria Ceballos"},
        "address": "San Martin 122",
        "faculties": ["Firmar checkes", "Abrir cuentas corrientes"],
    }

    response = authenticated_api_client.post(url, data=data, format="json")
    assert response.status_code == 201


@pytest.mark.django_db
def test_members_and_admins_from_rut_society(authenticated_api_client):
    societe_rut_code = "12345678-A"
    admin_rut_code = "92345178-Z"
    member_rut_code = "22212118-d"

    member_actions = 100
    society_actions = 1000

    rut = Rut.objects.create(
        code=societe_rut_code,
        name="Nombre de la sociedad",
    )
    society = Society.objects.create(
        rut=rut,
        actions=society_actions,
    )

    create_admin_url = reverse("society-create-admin", kwargs={"pk": society.id})
    create_member_url = reverse("society-create-member", kwargs={"pk": society.id})

    admin_data = {
        "rut": {"code": admin_rut_code, "name": "Florencia Diaz"},
        "address": "La Plata 5120",
        "faculties": ["Firmar checkes", "Abrir cuentas corrientes"],
    }
    member_data = {
        "rut": {"code": member_rut_code, "name": "Benjamin Torres"},
        "address": "Avenida Venezuela 22",
        "actions": member_actions,
    }

    authenticated_api_client.post(create_admin_url, data=admin_data, format="json")
    authenticated_api_client.post(create_member_url, data=member_data, format="json")

    url = reverse("society-list")
    response = authenticated_api_client.get(url, params=urlencode({"rut": societe_rut_code}))
    assert response.status_code == 200

    response_society = response.data[0]
    assert response_society["rut"]["code"] == societe_rut_code
    assert response_society["admins"][0]["admin"]["rut"]["code"] == admin_rut_code
    assert response_society["members"][0]["member"]["rut"]["code"] == member_rut_code
    assert response_society["members"][0]["participation"] == f"{member_actions / society_actions * 100}%"
    

