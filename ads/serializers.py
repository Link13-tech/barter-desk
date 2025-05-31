from rest_framework import serializers
from .models import Ad, ExchangeProposal


class AdSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Ad
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at']


class ExchangeProposalSerializer(serializers.ModelSerializer):
    ad_sender = serializers.PrimaryKeyRelatedField(queryset=Ad.objects.all())
    ad_receiver = serializers.PrimaryKeyRelatedField(queryset=Ad.objects.all())
    status = serializers.CharField(read_only=True)

    class Meta:
        model = ExchangeProposal
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class ExchangeProposalStatusUpdateSerializer(serializers.ModelSerializer):
    STATUS_CHOICES = [
        ('accepted', 'Принято'),
        ('declined', 'Отклонено'),
    ]

    status = serializers.ChoiceField(
        choices=STATUS_CHOICES,
        help_text='Выберите один из вариантов: accepted (Принято) или declined (Отклонено).'
    )

    class Meta:
        model = ExchangeProposal
        fields = ['status']
