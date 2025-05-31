from django.contrib.auth.models import User
from django.core.paginator import Paginator
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

    search_query = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')
    condition_filter = request.GET.get('condition', '')

    if search_query:
        ads = ads.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

    if category_filter:
        ads = ads.filter(category=category_filter)

    if condition_filter:
        ads = ads.filter(condition=condition_filter)

    paginator = Paginator(ads, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Ad.objects.values_list('category', flat=True).distinct()
    conditions = [choice[0] for choice in Ad.CONDITION_CHOICES]

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'category_filter': category_filter,
        'condition_filter': condition_filter,
        'categories': categories,
        'conditions': conditions,
    }
    return render(request, 'ads/ad_list.html', context)


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
    proposals = ExchangeProposal.objects.filter(
        Q(ad_sender__user=request.user) | Q(ad_receiver__user=request.user)
    ).order_by('-created_at')

    sender_filter = request.GET.get('sender', '')
    receiver_filter = request.GET.get('receiver', '')
    status_filter = request.GET.get('status', '')

    if sender_filter:
        proposals = proposals.filter(ad_sender__user__id=sender_filter)
    if receiver_filter:
        proposals = proposals.filter(ad_receiver__user__id=receiver_filter)
    if status_filter:
        proposals = proposals.filter(status=status_filter)

    paginator = Paginator(proposals, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user_ads = Ad.objects.filter(user=request.user)

    users_sender = User.objects.filter(ads__sent_proposals__ad_receiver__user=request.user).distinct()
    users_receiver = User.objects.filter(ads__received_proposals__ad_sender__user=request.user).distinct()

    context = {
        'page_obj': page_obj,
        'user_ads': user_ads,
        'sender_filter': sender_filter,
        'receiver_filter': receiver_filter,
        'status_filter': status_filter,
        'users_sender': users_sender,
        'users_receiver': users_receiver,
    }
    return render(request, 'ads/exchange_proposals.html', context)


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
