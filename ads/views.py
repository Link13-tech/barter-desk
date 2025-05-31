from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Q
from .models import Ad, ExchangeProposal
from .forms import AdForm, ExchangeProposalForm


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('ad_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'users/profile.html')


def ad_list(request):
    ads = Ad.objects.all().order_by('-created_at')
    return render(request, 'ads/ad_list.html', {'ads': ads})


def ad_detail(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    return render(request, 'ads/ad_detail.html', {'ad': ad})


@login_required
def ad_create(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('ad_detail', pk=ad.pk)
    else:
        form = AdForm()
    return render(request, 'ads/ad_form.html', {'form': form})


@login_required
def ad_update(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if ad.user != request.user:
        return redirect('ad_detail', pk=pk)
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ad_detail', pk=pk)
    else:
        form = AdForm(instance=ad)
    return render(request, 'ads/ad_form.html', {'form': form})


@login_required
def ad_delete(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if ad.user == request.user:
        ad.delete()
    return redirect('ad_list')


@login_required
def create_exchange_proposal(request, ad_id):
    ad_receiver = get_object_or_404(Ad, pk=ad_id)

    if ad_receiver.user == request.user:
        return redirect('ad_detail', pk=ad_id)

    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST, user=request.user)
        if form.is_valid():
            ad_sender = form.cleaned_data['ad_sender']

            if ad_sender.user != request.user:
                form.add_error('ad_sender', 'Вы должны выбрать одно из своих объявлений.')
            else:
                exists = ExchangeProposal.objects.filter(
                    status='pending'
                ).filter(
                    Q(ad_sender=ad_sender, ad_receiver=ad_receiver) |
                    Q(ad_sender=ad_receiver, ad_receiver=ad_sender)
                ).exists()

                if exists:
                    form.add_error(None, "Уже существует активное предложение обмена между этими объявлениями.")
                else:
                    proposal = form.save(commit=False)
                    proposal.ad_sender = ad_sender
                    proposal.ad_receiver = ad_receiver
                    proposal.status = 'pending'
                    proposal.save()
                    return redirect('exchange_proposals_profile')
    else:
        form = ExchangeProposalForm(user=request.user)

    return render(request, 'ads/exchange_proposal_form.html', {'form': form, 'ad': ad_receiver})


@login_required
def exchange_proposals(request):
    sent = ExchangeProposal.objects.filter(ad_sender__user=request.user)
    received = ExchangeProposal.objects.filter(ad_receiver__user=request.user)
    return render(request, 'ads/exchange_proposals.html', {
        'sent': sent,
        'received': received,
    })


@login_required
def update_exchange_status(request, pk, status):
    proposal = get_object_or_404(ExchangeProposal, pk=pk)
    print(f"Updating proposal {proposal.pk} from {proposal.status} to {status}")  # debug

    if proposal.ad_receiver.user != request.user:
        print("User is not receiver, redirecting")
        return redirect('exchange_proposals_profile')

    if status in ['accepted', 'declined']:
        proposal.status = status
        proposal.save()
        print(f"Proposal status updated to {proposal.status}")

    return redirect('exchange_proposals_profile')
