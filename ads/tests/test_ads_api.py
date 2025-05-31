import pytest
from ads.models import Ad


@pytest.mark.django_db
def test_api_create_ad(auth_client):
    response = auth_client.post('/api/ads/', {
        'title': 'API Ad',
        'description': 'API Desc',
        'category': 'books',
        'condition': 'new'
    })
    if response.status_code != 201:
        print('Create Ad errors:', response.status_code, response.json())
    assert response.status_code == 201
    assert Ad.objects.filter(title='API Ad').exists()


@pytest.mark.django_db
def test_api_update_ad(auth_client, ad):
    url = f'/api/ads/{ad.id}/'
    response = auth_client.put(url, {
        'title': 'Updated API',
        'description': 'New desc',
        'category': 'electronics',
        'condition': 'used',
    })
    if response.status_code != 200:
        print('Update Ad errors:', response.status_code, response.json())
    ad.refresh_from_db()
    assert response.status_code == 200
    assert ad.title == 'Updated API'


@pytest.mark.django_db
def test_api_delete_ad(auth_client, ad):
    url = f'/api/ads/{ad.id}/'
    response = auth_client.delete(url)
    if response.status_code != 204:
        print('Delete Ad errors:', response.status_code, response.content)
    assert response.status_code == 204
    assert not Ad.objects.filter(id=ad.id).exists()
