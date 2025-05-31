import pytest
from django.urls import reverse
from ads.models import Ad


@pytest.mark.django_db
def test_ad_list_view(client):
    response = client.get(reverse('ad_list'))
    assert response.status_code == 200
    assert 'Объявления' in response.content.decode()


@pytest.mark.django_db
def test_ad_create_view(client, user):
    client.login(username='user1', password='pass')
    response = client.post(reverse('ad_create'), {
        'title': 'New Ad',
        'description': 'Text',
        'category': 'books',
        'condition': 'new'
    })
    if response.status_code != 302:
        print('Create View errors:', response.status_code, response.content.decode())
    assert response.status_code == 302
    assert Ad.objects.filter(title='New Ad').exists()


@pytest.mark.django_db
def test_ad_update_view(client, user, ad):
    client.login(username='user1', password='pass')
    url = reverse('ad_update', args=[ad.id])
    response = client.post(url, {'title': 'Updated', 'description': 'D', 'category': 'books', 'condition': 'new'})
    if response.status_code != 302:
        print('Update View errors:', response.status_code, response.content.decode())
    ad.refresh_from_db()
    assert response.status_code == 302
    assert ad.title == 'Updated'


@pytest.mark.django_db
def test_ad_delete_view(client, user, ad):
    client.login(username='user1', password='pass')
    url = reverse('ad_delete', args=[ad.id])
    response = client.post(url)
    if response.status_code != 302:
        print('Delete View errors:', response.status_code, response.content.decode())
    assert response.status_code == 302
    assert not Ad.objects.filter(id=ad.id).exists()
