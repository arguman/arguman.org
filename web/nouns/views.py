from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import get_language
from django.views.generic import DetailView, CreateView, ListView
from i18n.utils import normalize_language_code
from nouns.models import Noun, Relation, Channel
from nouns.forms import RelationCreationForm
from premises.models import Contention
from premises.views import HomeView
from profiles.mixins import LoginRequiredMixin


class NounDetail(DetailView):
    queryset = (Noun
                .objects
                .prefetch_related('contentions')
                .select_related('contentions__user')
                .order_by('-date_creation'))
    template_name = "nouns/detail.html"
    partial_template_name = "nouns/partial.html"
    context_object_name = "noun"

    def get_template_names(self):
        if self.request.GET.get('partial'):
            return [self.partial_template_name]
        return [self.template_name]

    def get_context_data(self, **kwargs):
        contentions = (self.get_object().active_contentions())
        indirect_contentions = (self.get_object().indirect_contentions())
        source = self.request.GET.get('source')
        if source:
            contentions = contentions.exclude(id=source)
            indirect_contentions = indirect_contentions.exclude(id=source)
        return super(NounDetail, self).get_context_data(
            contentions=contentions,
            indirect_contentions=indirect_contentions,
            **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(
            self.queryset,
            slug=self.kwargs['slug'],
            language=normalize_language_code(get_language())
        )


class RelationCreate(LoginRequiredMixin, CreateView):
    model = Relation
    template_name = "nouns/new_relation.html"
    form_class = RelationCreationForm
    initial = {
        'relation_type': Relation.HYPERNYM
    }

    def form_valid(self, form):
        form.instance.source = self.get_noun()
        form.instance.target = form.get_target()
        form.instance.user = self.request.user
        form.instance.is_active = False
        form.save()
        return redirect(form.instance.source)

    def get_context_data(self, **kwargs):
        noun = self.get_noun()
        return super(RelationCreate, self).get_context_data(
            noun=noun, **kwargs)

    def get_noun(self):
        return get_object_or_404(Noun, slug=self.kwargs.get('slug'))


class ChannelDetail(HomeView):
    template_name = "nouns/channel_detail.html"
    paginate_by = 20
    context_object_name = "contentions"

    def get_channel(self):
        language = normalize_language_code(get_language())
        return get_object_or_404(Channel, slug=self.kwargs['slug'],
                                 language=language)

    def get_context_data(self, **kwargs):
        channel = self.get_channel()
        return super(ChannelDetail, self).get_context_data(
            channel=channel, **kwargs)

    def get_contentions(self, paginate=True):
        channel = self.get_channel()
        nouns = channel.nouns.all()
        contentions = (Contention
                       .objects
                       .language()
                       .filter(is_featured=True,
                               nouns__in=nouns)
                       .distinct()
                       .order_by("-date_modification"))

        if paginate:
            contentions = (contentions[self.get_offset(): self.get_limit()])

        return contentions
