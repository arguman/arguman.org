from django.contrib import admin
from django.db.models import Q
from django.http import HttpResponseRedirect

from django.utils.translation import get_language

from i18n.utils import normalize_language_code
from nouns.models import Noun, Keyword, Relation, Channel
from premises.models import Contention


class KeywordInline(admin.TabularInline):
    model = Keyword
    extra = 0


class ContentionInline(admin.TabularInline):
    model = Contention.nouns.through
    extra = 0
    raw_id_fields = ('contention',)


class RelationInline(admin.TabularInline):
    model = Relation
    extra = 0
    raw_id_fields = ('target', 'user')
    fk_name = 'source'


class ActionInChangeFormMixin(object):
    def response_action(self, request, queryset):
        """
        Prefer http referer for redirect
        """
        _super = super(ActionInChangeFormMixin, self)
        response = _super.response_action(request, queryset)
        if isinstance(response, HttpResponseRedirect):
            response['Location'] = request.META.get(
                                'HTTP_REFERER', response.url)
        return response  

    def change_view(self, request, object_id, extra_context=None):
        actions = self.get_actions(request)
        if actions:
            action_form = self.action_form(auto_id=None)
            choices = self.get_action_choices(request)
            action_form.fields['action'].choices = choices
        else: 
            action_form = None
        extra_context=extra_context or {}
        extra_context['action_form'] = action_form
        return super(ActionInChangeFormMixin, self).change_view(
                      request, object_id, extra_context=extra_context)


class NounAdmin(ActionInChangeFormMixin, admin.ModelAdmin):
    list_display = ('__unicode__', 'is_active', 'hypernyms_as_text')
    list_filter = ('is_active', )
    inlines = [KeywordInline, ContentionInline, RelationInline]
    actions = ['update_contentions', 'reset_contentions',
               'update_with_wordnet', 'make_active', 'make_passive']
    search_fields = ['text', 'keywords__text']
    actions_on_top = True
    actions_on_bottom = True
    save_on_top = True

    def get_form(self, request, obj=None, **kwargs):
        form = super(NounAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['language'].initial = normalize_language_code(get_language())
        return form

    def get_queryset(self, request):
        qs = super(NounAdmin, self).get_queryset(request)
        return qs.prefetch_related('out_relations', 'keywords')

    def update_contentions(self, request, qs):
        q = Q()

        for noun in qs:
            q |= Q(title__icontains=noun.text)
            for keyword in noun.keywords.all():
                q |= Q(title__icontains=keyword.text)

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
             'id': hypernym.target.id,
             'text': hypernym.target.text
         } for hypernym in noun.hypernyms()])

    hypernyms_as_text.allow_tags = True

    def make_active(self, request, qs):
        return qs.update(is_active=True)

    def make_passive(self, request, qs):
        return qs.update(is_active=False)


class ChannelAdmin(admin.ModelAdmin):
    filter_horizontal = ('nouns', )


admin.site.register(Noun, NounAdmin)
admin.site.register(Channel, ChannelAdmin)
