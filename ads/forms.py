from django import forms
from .models import Ad, ExchangeProposal


class AdForm(forms.ModelForm):
    image_url = forms.URLField(assume_scheme='https', required=False)

    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']


class ExchangeProposalForm(forms.ModelForm):
    ad_sender = forms.ModelChoiceField(queryset=Ad.objects.none(), label="Ваше объявление")

    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'comment']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['ad_sender'].queryset = Ad.objects.filter(user=user)
