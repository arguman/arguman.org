from django import forms

from premises.models import Contention


class ArgumentCreationForm(forms.ModelForm):
    class Meta:
        model = Contention
        fields = ['title', 'description', 'owner', 'sources']
