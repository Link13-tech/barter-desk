import pytest
from django.urls import reverse
from ads.models import ExchangeProposal


@pytest.mark.django_db
def test_create_exchange_proposal_view(client, user, ad, another_user, another_ad):
    client.force_login(user)
    url = reverse('create_exchange_proposal', kwargs={'ad_id': another_ad.pk})

    # GET - форма должна открыться
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context

    response = client.post(url, data={'ad_sender': ad.pk, 'comment': 'Обменяюсь'})
    assert response.status_code == 302

    proposal = ExchangeProposal.objects.filter(ad_sender=ad, ad_receiver=another_ad).first()
    assert proposal is not None
    assert proposal.status == 'pending'
    assert proposal.comment == 'Обменяюсь'


@pytest.mark.django_db
def test_update_exchange_status(client, user, another_user, proposal):

    client.force_login(user)
    url = reverse('update_exchange_status_profile', kwargs={'pk': proposal.pk, 'status': 'accepted'})
    response = client.get(url)
    assert response.status_code == 302
    proposal.refresh_from_db()
    assert proposal.status == 'pending'

    client.force_login(another_user)
    url = reverse('update_exchange_status_profile', kwargs={'pk': proposal.pk, 'status': 'accepted'})
    response = client.get(url)
    assert response.status_code == 302
    proposal.refresh_from_db()
    assert proposal.status == 'accepted'
