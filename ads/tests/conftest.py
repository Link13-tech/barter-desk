import pytest
from django.contrib.auth.models import User
from ads.models import Ad, ExchangeProposal
from rest_framework.test import APIClient


@pytest.fixture
def user(db):
    return User.objects.create_user(username='user1', password='pass')


@pytest.fixture
def another_user(db):
    return User.objects.create_user(username='user2', password='testpass')


@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def auth_client_another_user(another_user):
    client = APIClient()
    client.force_authenticate(user=another_user)
    return client


@pytest.fixture
def ad(user):
    return Ad.objects.create(
        user=user,
        title='Test Ad',
        description='Some desc',
        category='books',
        condition='new',
    )


@pytest.fixture
def another_ad(another_user):
    return Ad.objects.create(
        user=another_user,
        title='Another Ad',
        description='Second ad',
        category='electronics',
        condition='new',
    )


@pytest.fixture
def proposal(ad, another_ad):
    return ExchangeProposal.objects.create(
        ad_sender=ad,
        ad_receiver=another_ad,
        comment="Test proposal",
        status='pending'
    )
