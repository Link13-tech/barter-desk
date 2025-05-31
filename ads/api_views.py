from django.core.exceptions import PermissionDenied
from django.db import models
from django.db.models import Q
from rest_framework import generics, permissions, filters
from rest_framework.exceptions import ValidationError

from .models import Ad, ExchangeProposal
from .serializers import AdSerializer, ExchangeProposalSerializer, ExchangeProposalStatusUpdateSerializer


class AdListCreateAPIView(generics.ListCreateAPIView):
    queryset = Ad.objects.all().order_by('-created_at')
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'category', 'condition']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AdRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if self.get_object().user != self.request.user:
            raise PermissionDenied("Вы не автор этого объявления")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("Вы не автор этого объявления")
        instance.delete()


class ExchangeProposalCreateAPIView(generics.CreateAPIView):
    queryset = ExchangeProposal.objects.all()
    serializer_class = ExchangeProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        ad_sender = serializer.validated_data['ad_sender']
        ad_receiver = serializer.validated_data['ad_receiver']

        if ad_sender.user != self.request.user:
            raise PermissionDenied("Вы не владелец объявления-отправителя.")

        if ad_receiver.user == self.request.user:
            raise ValidationError("Нельзя отправить предложение самому себе.")

        exists = ExchangeProposal.objects.filter(
            status='pending'
        ).filter(
            Q(ad_sender=ad_sender, ad_receiver=ad_receiver) |
            Q(ad_sender=ad_receiver, ad_receiver=ad_sender)
        ).exists()

        if exists:
            raise ValidationError("Уже существует активное предложение обмена между этими объявлениями.")

        serializer.save(status='pending')


class ExchangeProposalListAPIView(generics.ListAPIView):
    serializer_class = ExchangeProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ExchangeProposal.objects.filter(
            models.Q(ad_sender__user=user) | models.Q(ad_receiver__user=user)
        )


class ExchangeProposalUpdateStatusAPIView(generics.UpdateAPIView):
    queryset = ExchangeProposal.objects.all()
    serializer_class = ExchangeProposalStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        proposal = self.get_object()
        if proposal.ad_receiver.user != self.request.user:
            raise PermissionDenied("Только получатель может изменить статус.")
        serializer.save()
