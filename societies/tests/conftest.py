import os
import django
import pytest
from django.core.management import call_command
from rest_framework.test import APIClient
from django.contrib.auth.models import User

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "legalbot.settings")
django.setup()


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("migrate")


@pytest.fixture
def enable_db_access_for_all_tests(django_db_setup):
    pass


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="testpassword")


@pytest.fixture
def authenticated_api_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client
