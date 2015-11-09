# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import get_language

from i18n.utils import normalize_language_code
from premises.mixins import FormRenderer
from nouns.models import Relation, Noun


class RelationCreationForm(FormRenderer, forms.ModelForm):
    target_noun = forms.CharField()
    relation_type = forms.ChoiceField(
        choices=Relation.TYPES, widget=forms.RadioSelect)

    class Meta:
        model = Relation
        fields = ['relation_type']

    def clean_target_noun(self):
        target_noun = self.cleaned_data['target_noun']
        return (target_noun
                 .lower()
                 .strip())

    def get_target(self):
        target_noun = self.cleaned_data['target_noun']

        try:
            noun = Noun.objects.get(
                text=target_noun,
                language=normalize_language_code(get_language())
            )
        except Noun.DoesNotExist:
            noun = Noun.objects.create(
                text=target_noun,
                is_active=False,
                language=normalize_language_code(get_language())
            )

        return noun
