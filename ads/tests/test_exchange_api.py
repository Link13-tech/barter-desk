import pytest
from ads.models import ExchangeProposal


@pytest.mark.django_db
def test_create_exchange_proposal(auth_client, ad, another_ad):
    response = auth_client.post('/api/proposals/create/', {
        'ad_sender': ad.id,
        'ad_receiver': another_ad.id,
        'comment': 'Test comment',
        'status': 'pending'
    })
    if response.status_code != 201:
        print('Create Proposal errors:', response.status_code, response.json())
    assert response.status_code == 201
    assert ExchangeProposal.objects.count() == 1


@pytest.mark.django_db
def test_update_exchange_status(auth_client_another_user, proposal):
    url = f'/api/proposals/{proposal.pk}/update-status/'
    response = auth_client_another_user.patch(url, {'status': 'accepted'})
    if response.status_code != 200:
        print('Update Proposal errors:', response.status_code, response.content.decode())
    proposal.refresh_from_db()
    assert response.status_code == 200
    assert proposal.status == 'accepted'
