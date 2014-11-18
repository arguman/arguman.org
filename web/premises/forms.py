# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from premises.constants import MAX_PREMISE_CONTENT_LENGTH

from premises.mixins import FormRenderer
from premises.models import Contention, Premise, Report


class ArgumentCreationForm(FormRenderer, forms.ModelForm):
    class Meta:
        model = Contention
        fields = ['title', 'owner', 'sources']


class PremiseCreationForm(FormRenderer, forms.ModelForm):

    class Meta:
        model = Premise
        fields = ['premise_type', 'text', 'sources']
        widgets = {
            'premise_type': forms.RadioSelect,
            'text': forms.Textarea(attrs={
                'maxlength': MAX_PREMISE_CONTENT_LENGTH
            })
        }


class PremiseEditForm(FormRenderer, forms.ModelForm):
    class Meta:
        model = Premise
        fields = ['premise_type', 'text', 'sources', 'parent', 'is_approved']
        widgets = {
            'premise_type': forms.RadioSelect
        }

    def __init__(self, *args, **kwargs):
        super(PremiseEditForm, self).__init__(*args, **kwargs)
        queryset = (self.instance
          .argument
          .premises
          .exclude(pk=self.instance.pk))  # avoid self-loop
        self.fields['parent'].queryset = queryset


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["fallacy_type"]

    def clean(self):
        is_report_exist = Report.objects.filter(
            reporter=self.initial['reporter'],
            premise=self.initial['premise'],
            contention=self.initial['contention'],
            fallacy_type=self.cleaned_data['fallacy_type']
        ).exists()
        if is_report_exist:
            raise ValidationError(u'Bu safsata bildirimini zaten yaptınız.')

        super(ReportForm, self).clean()