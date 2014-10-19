from django import forms

from premises.models import Contention, Premise


class ArgumentCreationForm(forms.ModelForm):
    class Meta:
        model = Contention
        fields = ['title', 'description', 'owner', 'sources']


class PremiseCreationForm(forms.ModelForm):
    class Meta:
        model = Premise
        fields = ['premise_type', 'text', 'sources']


class PremiseEditForm(forms.ModelForm):
    class Meta:
        model = Premise
        fields = ['premise_type', 'text', 'sources', 'is_approved']
