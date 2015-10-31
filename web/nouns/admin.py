from django.contrib import admin
from django.db.models import Count, Q
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms

from nouns.models import Noun, Synonym
from premises.models import Contention


class SynonymInline(admin.TabularInline):
    model = Synonym
    extra = 0


class ContentionInline(admin.TabularInline):
    model = Contention.nouns.through
    extra = 0
    raw_id_fields = ('contention',)


class HypernymsInline(admin.SimpleListFilter):
    parameter_name = 'hypernym'
    root_hypernym = 'abstraction'
    title = 'hypernym'

    def lookups(self, request, model_admin):
        if self.value():
            hyponyms = Noun.objects.filter(
                hypernyms__id=self.value())
        else:
            hyponyms = Noun.objects.filter(
                hypernyms__text=self.root_hypernym)

        return [
            (hyponym.id, hyponym.text)
            for hyponym in hyponyms
            ]

    def queryset(self, request, qs):
        if not self.value():
            return qs

        return qs.filter(hypernyms__id=self.value())


class NounAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'is_active', 'hypernyms_as_text')
    filter_horizontal = ('hypernyms',)
    list_filter = (HypernymsInline, 'is_active')
    inlines = [SynonymInline, ContentionInline]
    actions = ['update_contentions', 'reset_contentions',
               'update_with_wordnet', 'make_active', 'make_passive']
    search_fields = ['text', 'synonyms__text']

    def get_queryset(self, request):
        qs = super(NounAdmin, self).get_queryset(request)
        return qs.prefetch_related('hypernyms', 'synonyms')

    def update_contentions(self, request, qs):
        q = Q()

        for noun in qs:
            q |= Q(title__icontains=noun.text)
            for synonym in noun.synonyms.all():
                q |= Q(title__icontains=synonym.text)

        contentions = Contention.objects.filter(q)
        for contention in contentions:
            contention.save_nouns()

    def reset_contentions(self, request, qs):
        contentions = Contention.objects.filter(nouns=qs)
        for contention in contentions:
            contention.nouns.clear()

    def update_with_wordnet(self, request, qs):
        for noun in qs:
            noun.update_with_wordnet()

    def hypernyms_as_text(self, noun):
        return ', '.join([
                             '<a href="%(id)s">%(text)s</a>' % {
                                 'id': hypernym.id,
                                 'text': hypernym.text
                             } for hypernym in noun.hypernyms.all()
                             ])

    hypernyms_as_text.allow_tags = True

    def make_active(self, request, qs):
        return qs.update(is_active=True)

    def make_passive(self, request, qs):
        return qs.update(is_active=False)


admin.site.register(Noun, NounAdmin)
