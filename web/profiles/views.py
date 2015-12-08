import json
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.utils.translation import get_language
from django.views.generic import (
    FormView, CreateView, RedirectView, DetailView, UpdateView)
from django.db.models import Q, Count
from networkx import DiGraph
from networkx.readwrite import json_graph
from i18n.utils import normalize_language_code
from nouns.models import Noun, Channel

from profiles.mixins import LoginRequiredMixin
from profiles.forms import (RegistrationForm, AuthenticationForm,
                            ProfileUpdateForm)
from profiles.models import Profile
from premises.models import Contention, Premise, SUPPORT, OBJECTION, SITUATION, Report
from premises.mixins import PaginationMixin
from newsfeed.models import Entry


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = "auth/register.html"

    def form_valid(self, form):
        response = super(RegistrationView, self).form_valid(form)
        user = authenticate(username=form.cleaned_data["username"],
                            password=form.cleaned_data["password1"])
        login(self.request, user)
        return response

    def get_success_url(self):
        return reverse("home")


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = "auth/login.html"

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        return self.request.GET.get("next") or reverse("home")

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context["next"] = self.request.GET.get("next", "")
        return context


class LogoutView(LoginRequiredMixin, RedirectView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        return reverse("home")


class BaseProfileDetailView(DetailView):
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = "profile"
    model = Profile
    paginate_by = 20
    tab_name = "overview"

    def get_context_data(self, **kwargs):
        """
        Adds extra context to template
        """
        user = self.get_object()

        can_follow = self.request.user != user

        if self.request.user.is_authenticated():
            is_followed = self.request.user.following.filter(
                pk=user.id).exists()
        else:
            is_followed = False

        return super(BaseProfileDetailView, self).get_context_data(
            can_follow=can_follow,
            is_followed=is_followed,
            tab_name=self.tab_name,
            **kwargs
        )


class ProfileDetailView(BaseProfileDetailView):
    def get_context_data(self, **kwargs):
        """
        Adds extra context to template
        """
        user = self.get_object()
        return super(ProfileDetailView, self).get_context_data(
            related_channels=self.get_related_channels(user),
            discussed_users=self.get_discussed_users(user),
            supported_premises=self.get_supported_premises(user),
            **kwargs
        )

    def get_supported_premises(self, user):
        return Premise.objects.filter(
            is_approved=True,
            user=user,
            argument__language=normalize_language_code(get_language())
        ).annotate(
            supporter_count=Count('supporters', distinct=True)
        ).filter(
            supporter_count__gt=0
        ).order_by(
            '-supporter_count'
        )[:10]

    def get_discussed_users(self, user):
        lines = Premise.objects.filter(
            user=user,
            parent__user__isnull=False,
        ).exclude(
            parent__user=user
        ).values(
            'parent__user'
        ).annotate(
            count=Count('parent__user')
        ).order_by(
            '-count'
        )[:5]

        profiles = [Profile.objects.get(id=line['parent__user'])
                    for line in lines]

        def make_bundle(target):
            because = self.premise_count_by_user(user, target, SUPPORT)
            but = self.premise_count_by_user(user, target, OBJECTION)
            however = self.premise_count_by_user(user, target, SITUATION)
            total = because + but + however

            return {
                'user': profile,
                'because': 100 * float(because) / total,
                'but': 100 * float(but) / total,
                'however': 100 * float(however) / total
            }

        return [
            make_bundle(profile)
            for profile in profiles
        ]

    def premise_count_by_user(self, user, target, premise_type):
        return Premise.objects.filter(
            user=user,
            parent__user=target,
            premise_type=premise_type
        ).count()

    def get_related_channels(self, user):
        contention_nouns = Contention.objects.filter(
            premises__user=user,
            nouns__isnull=False,
            language=normalize_language_code(get_language())
        ).order_by(
            '-premises__weight'
        ).values_list(
            'nouns',
            flat=True
        )

        supported_nouns = Contention.objects.filter(
            premises__supporters=user,
            nouns__isnull=False,
            language=normalize_language_code(get_language())
        ).order_by(
            '-premises__weight'
        ).values_list(
            'nouns',
            flat=True
        )

        noun_ids = list(contention_nouns) + list(supported_nouns)
        noun_set = set(noun_ids)

        channels = Channel.objects.filter(
            nouns__in=noun_ids,
            language=normalize_language_code(get_language())
        ).distinct()

        bundle = []
        total_score = 0

        for channel in channels:
            channel_dict = {
                'channel': channel.serialize(),
                'score': 0,
            }

            for noun in channel.nouns.all():
                if noun.pk in noun_set:
                    channel_dict['score'] += noun_ids.count(noun.pk)

            total_score += channel_dict['score']

            bundle.append(channel_dict)

        return sorted(bundle,
                      key=lambda c: c['score'],
                      reverse=True)


class ProfileArgumentsView(BaseProfileDetailView):
    tab_name = "arguments"
    template_name = "auth/contentions.html"

    def get_context_data(self, **kwargs):
        user = self.get_object()
        contentions = Contention.objects.filter(
            user=user
        ).order_by("-date_creation")

        if user != self.request.user:
            contentions = contentions.filter(is_published=True)

        return super(ProfileArgumentsView, self).get_context_data(
            contentions=contentions
        )


class ProfileFallaciesView(BaseProfileDetailView):
    tab_name = "fallacies"
    template_name = "auth/fallacies.html"

    def get_context_data(self, **kwargs):
        user = self.get_object()
        fallacies = Report.objects.filter(
            reason__isnull=False,
            reporter=user
        ).order_by('-id')

        return super(ProfileFallaciesView, self).get_context_data(
            fallacies=fallacies
        )


class ProfilePremisesView(BaseProfileDetailView, PaginationMixin):
    tab_name = "premises"
    template_name = "auth/premises.html"
    paginate_by = 20

    def get_objects(self, paginate=True):
        user = self.get_object()
        premises = Premise.objects.filter(user=user).order_by("-date_creation")

        if user != self.request.user:
            premises = premises.filter(is_approved=True)

        if paginate:
            premises = premises[self.get_offset():self.get_limit()]

        return premises

    def has_next_page(self):
        total = self.get_objects(paginate=False).count()
        return total > (self.get_offset() + self.paginate_by)

    def get_context_data(self, **kwargs):
        premises = self.get_objects()

        return super(ProfilePremisesView, self).get_context_data(
            premises=premises,
            has_next_page=self.has_next_page(),
            next_page_url=self.get_next_page_url(),
        )


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProfileUpdateForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return self.request.user.get_absolute_url()


class ProfileChannelsGraphView(ProfileDetailView):
    def render_to_response(self, context, **response_kwargs):
        user = self.get_object()
        return HttpResponse(json.dumps(self.get_bundle(user)),
                            content_type="application/json")

    def get_bundle(self, user):
        graph = self.build_graph(user)
        return json_graph.node_link_data(graph)

    def build_graph(self, user):
        contention_nouns = Contention.objects.filter(
            premises__user=user,
            nouns__isnull=False,
            language=normalize_language_code(get_language())
        ).order_by(
            '-premises__weight'
        ).values_list(
            'nouns',
            flat=True
        )

        supported_nouns = Contention.objects.filter(
            premises__supporters=user,
            nouns__isnull=False,
            language=normalize_language_code(get_language())
        ).order_by(
            '-premises__weight'
        ).values_list(
            'nouns',
            flat=True
        )

        noun_ids = set(contention_nouns) ^ set(supported_nouns)

        channels = Channel.objects.filter(
            nouns__in=noun_ids,
            language=normalize_language_code(get_language())
        ).distinct()

        graph = DiGraph()

        last_channel = None
        first_channel = None

        label = lambda x: x.title()

        for channel in channels:
            graph.add_node(channel.title, {
                "label": label(channel.title),
                "type": "channel"
            })

            if last_channel:
                graph.add_edge(last_channel.title, channel.title)

            channel_nouns = channel.nouns.all()
            for channel_noun in channel_nouns:

                if channel_noun.id in noun_ids:
                    graph.add_edge(channel_noun.text, channel.title)

                    graph.add_node(channel_noun.text, {
                        "label": label(channel_noun.text),
                        "type": "noun"
                    })

            last_channel = channel
            if not first_channel:
                first_channel = channel

        graph.add_edge(first_channel.title, last_channel.title)

        return graph
