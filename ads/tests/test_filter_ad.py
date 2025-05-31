import pytest
from django.urls import reverse
from ads.models import Ad


@pytest.mark.django_db
def test_ad_list_search(client, user, ad):
    client.force_login(user)
    url = reverse('ad_list')

    # Поиск по части названия из фикстуры
    response = client.get(url + f'?q={ad.title[:4]}')
    assert response.status_code == 200
    ads_found = response.context['page_obj'].object_list
    assert any(a.pk == ad.pk for a in ads_found)
