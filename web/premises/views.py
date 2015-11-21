# -*- coding:utf-8 -*-

import json
from datetime import timedelta
from django.conf import settings
from markdown2 import markdown

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.db.models import Max, Sum
from django.utils.timezone import now
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views.generic import DetailView, TemplateView, CreateView, View
from django.views.generic.edit import UpdateView
from django.utils.translation import get_language
from django.db.models import Count
from django.shortcuts import render

from blog.models import Post
from communities.mixins import CommunityMixin
from premises.models import Contention, Premise
from premises.forms import (ArgumentCreationForm, PremiseCreationForm,
                            PremiseEditForm, ReportForm)
from premises.signals import (added_premise_for_premise,
                              added_premise_for_contention,
                              reported_as_fallacy,
                              supported_a_premise)
from premises.templatetags.premise_tags import check_content_deletion
from premises.mixins import PaginationMixin, NextURLMixin
from newsfeed.models import Entry
from profiles.mixins import LoginRequiredMixin
from profiles.models import Profile
from nouns.models import Channel

from i18n.utils import normalize_language_code


def get_ip_address(request):
    return (request.META.get('HTTP_X_FORWARDED_FOR') or
            request.META.get('REMOTE_ADDR'))


class ContentionDetailView(DetailView):
    queryset = (Contention.objects
                .select_related('user')
                .prefetch_related('premises'))
    context_object_name = 'contention'

    def get_template_names(self):
        view = self.request.GET.get("view")
        name = ("list_view" if view == "list" else "tree_view")
        return ["premises/%s.html" % name]

    def get_parent(self):
        premise_id = self.kwargs.get("premise_id")
        if premise_id:
            return get_object_or_404(Premise, id=premise_id)

    def get_premises(self):
        contention = self.get_parent() or self.get_object()
        return contention.published_children()

    def get_context_data(self, **kwargs):
        contention = self.get_object()
        edit_mode = (
            self.request.user.is_superuser or
            self.request.user.is_staff or
            contention.user == self.request.user)
        return super(ContentionDetailView, self).get_context_data(
            premises=self.get_premises(),
            parent_premise=self.get_parent(),
            path=contention.get_absolute_url(),
            edit_mode=edit_mode,
            serialized=contention.serialize(self.request.user),
            **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        host = request.META['HTTP_HOST']

        if not host.startswith(settings.AVAILABLE_LANGUAGES):
            return redirect(self.object.get_full_url())

        if not normalize_language_code(get_language()) == self.object.language:
            return redirect(self.object.get_full_url())

        partial = request.GET.get('partial')
        level = request.GET.get('level')

        if partial:
            contention = self.object

            try:
                serialized = contention.partial_serialize(int(partial), self.request.user)
            except (StopIteration, ValueError):
                raise Http404

            return render(request, 'premises/tree.html', {
                'premises': serialized['premises'],
                'serialized': serialized,
                'level': int(level)
            })

        return super(ContentionDetailView, self).get(request, *args, **kwargs)


class ContentionJsonView(DetailView):
    model = Contention

    def render_to_response(self, context, **response_kwargs):
        contention = self.get_object(self.get_queryset())
        return HttpResponse(json.dumps({
            "nodes": self.build_tree(contention, self.request.user),
        }), content_type="application/json")

    def build_tree(self, contention, user):
        return {
            "name": contention.title,
            "parent": None,
            "pk": contention.pk,
            "owner": contention.owner,
            "sources": contention.sources,
            "is_singular": self.is_singular(contention),
            "children": self.get_premises(contention, user)
        }

    def get_premises(self, contention, user, parent=None):
        children = [{
            "pk": premise.pk,
            "name": premise.text,
            "parent": parent.text if parent else None,
            "reportable_by_authenticated_user": self.user_can_report(
                premise, user),
            "report_count": premise.reports.count(),
            "user": {
                "id": premise.user.id,
                "username": premise.user.username,
                "absolute_url": reverse("auth_profile",
                                        args=[premise.user.username])
            },
            "sources": premise.sources,
            "premise_type": premise.premise_class(),
            "children": (self.get_premises(contention, user, parent=premise)
                         if premise.published_children().exists() else [])
        } for premise in contention.published_premises(parent)]
        return children

    def user_can_report(self, premise, user):
        if user.is_authenticated() and user != premise.user:
            return not premise.reported_by(user)

        return False

    def is_singular(self, contention):
        result = contention.premises.all().aggregate(
            max_sibling=Max('sibling_count'))
        return result['max_sibling'] <= 1


class HomeView(CommunityMixin, TemplateView, PaginationMixin):
    template_name = "index.html"
    tab_class = "featured"

    paginate_by = 20

    def get_context_data(self, **kwargs):
        contentions = self.get_contentions()
        if self.request.user.is_authenticated():
            notifications_qs = self.get_unread_notifications()
            notifications = list(notifications_qs)
            self.mark_as_read(notifications_qs)
        else:
            notifications = None
        return super(HomeView, self).get_context_data(
            channels=self.get_channels(),
            next_page_url=self.get_next_page_url(),
            tab_class=self.tab_class,
            notifications=notifications,
            has_next_page=self.has_next_page(),
            announcements=self.get_announcements(),
            contentions=contentions, **kwargs)

    def get_announcements(self):
        return Post.objects.filter(is_announcement=True)

    def get_unread_notifications(self):
        return (self.request.user
                .notifications
                .filter(is_read=False)[:5])

    def mark_as_read(self, notifications):
        pks = notifications.values_list("id", flat=True)
        (self.request.user
         .notifications
         .filter(id__in=pks)
         .update(is_read=True))

    def get_contentions(self, paginate=True):
        contentions = (Contention
                       .objects
                       .language()
                       .filter(is_featured=True)
                       .order_by("-date_modification"))

        contentions = self.apply_community_filter(contentions)

        if paginate:
            contentions = (contentions[self.get_offset(): self.get_limit()])

        return contentions

    def get_channels(self):
        return Channel.objects.filter(
            community=self.request.community,
            language=normalize_language_code(get_language())
        ).order_by('order')


class NotificationsView(LoginRequiredMixin, HomeView):
    template_name = "notifications.html"

    def get_context_data(self, **kwargs):
        notifications_qs = self.request.user.notifications.all()[:40]
        notifications = list(notifications_qs)
        self.mark_as_read(notifications_qs)
        return super(HomeView, self).get_context_data(
            notifications=notifications,
            **kwargs)


class SearchView(HomeView):
    tab_class = 'search'
    template_name = 'search/search.html'
    partial_templates = {
        'contentions': 'search/contention.html',
        'users': 'search/profile.html',
        'premises': 'search/premise.html'
    }

    method_mapping = {'contentions': "get_contentions",
                      'users': "get_users",
                      'premises': "get_premises"}

    def dispatch(self, request, *args, **kwargs):
        self.type = request.GET.get('type', 'contentions')

        if not self.method_mapping.get(self.type):
            raise Http404()
        return super(SearchView, self).dispatch(request, *args, **kwargs)

    def get_keywords(self):
        return self.request.GET.get('keywords') or ""

    def has_next_page(self):
        method = getattr(self, self.method_mapping[self.type])
        total = method().count()
        return total > (self.get_offset() + self.paginate_by)

    def get_search_bundle(self):
        method = getattr(self, self.method_mapping[self.type])
        return [{'template': self.partial_templates[self.type],
                'object': item} for item in method()]

    def get_context_data(self, **kwargs):
        return super(SearchView, self).get_context_data(
            results=self.get_search_bundle(),
            **kwargs)

    def get_next_page_url(self):
        offset = self.get_offset() + self.paginate_by
        return '?offset=%(offset)s&keywords=%(keywords)s&type=%(type)s' % {
            "offset": offset,
            "type": self.type,
            "keywords": self.get_keywords()
        }

    def get_premises(self, paginate=True):
        keywords = self.request.GET.get('keywords')
        if not keywords or len(keywords) < 3:
            result = Premise.objects.none()
        else:
            result = (Premise.objects.filter(
                argument__community=self.request.community,
                argument__language=normalize_language_code(get_language()),
                text__contains=keywords))
            if paginate:
                result = result[self.get_offset():self.get_limit()]
        return result

    def get_users(self, paginate=True):
        keywords = self.request.GET.get('keywords')
        if not keywords or len(keywords) < 2:
            result = Profile.objects.none()
        else:
            result = (Profile.objects.filter(
                username__icontains=keywords))
            if paginate:
                result = result[self.get_offset():self.get_limit()]
        return result

    def get_contentions(self, paginate=True):
        keywords = self.request.GET.get('keywords')
        if not keywords or len(keywords) < 2:
            result = Contention.objects.none()
        else:
            result = (Contention
                      .objects
                      .filter(title__icontains=keywords,
                              language=normalize_language_code(get_language())))

            result = self.apply_community_filter(result)

            if paginate:
                result = result[self.get_offset():self.get_limit()]

        return result


class NewsView(HomeView):
    tab_class = "news"

    def get_contentions(self, paginate=True):
        contentions = (
            Contention
                .objects
                .language()
                .filter(is_published=True)
                .order_by('-date_modification')
        )

        contentions = self.apply_community_filter(contentions)

        if paginate:
            contentions = contentions[self.get_offset():self.get_limit()]

        return contentions


class StatsView(HomeView):
    tab_class = "stats"
    template_name = "stats.html"
    partial_templates = {
        Profile: "stats/profile.html",
        Contention: "stats/contention.html",
        Premise: "stats/premise.html",
    }

    method_mapping = {
        "active_users": "get_active_users",
        "user_karma": "get_user_karma",
        "disgraced_users": "get_disgraced_users",
        "supported_premises": "get_supported_premises",
        "fallacy_premises": "get_fallacy_premises",
        "crowded_contentions": "get_crowded_contentions",
    }

    time_ranges = [7, 30]

    def get_context_data(self, **kwargs):
        return super(StatsView, self).get_context_data(
            stats=self.get_stats_bundle(),
            stats_type=self.get_stats_type(),
            days=self.days,
            **kwargs)

    def get_stats_type(self):
        return self.request.GET.get("what")

    def build_time_filters(self, date_field="date_creation"):
        days = self.request.GET.get("days")

        if not days or days == "all":
            self.days = None
            return {}

        try:
            days = int(days)
        except (TypeError, ValueError):
            days = None

        if not days or days not in self.time_ranges:
            raise Http404()

        self.days = days

        field_expression = "%s__gt" % date_field

        return {
            field_expression: timezone.now() - timedelta(days=days)
        }

    def get_stats_bundle(self):
        stat_type = self.get_stats_type()
        if stat_type not in self.method_mapping:
            raise Http404()
        method = getattr(self, self.method_mapping[stat_type])
        return [
            {
                "template": self.partial_templates[type(item)],
                "object": item
            } for item in method()
        ]

    def get_active_users(self):
        return Profile.objects.annotate(
            premise_count=Sum("user_premises"),
        ).filter(
            premise_count__gt=0,
            **self.build_time_filters(date_field="user_premises__date_creation")
        ).order_by("-premise_count")[:10]

    def get_user_karma(self):
        return Profile.objects.\
                   filter(**self.build_time_filters(date_field="user_premises__date_creation")).\
                   order_by("-karma", "id").distinct()[:10]

    def get_disgraced_users(self):
        return Profile.objects.annotate(
            report_count=Sum("user_premises__reports"),
        ).filter(
            report_count__gt=0,
            **self.build_time_filters(date_field="user_premises__date_creation")
        ).order_by("-report_count")[:10]

    def get_supported_premises(self):
        return Premise.objects.annotate(
            supporter_count=Sum("supporters")
        ).filter(
            argument__community=self.request.community,
            argument__language=get_language(),
            supporter_count__gt=0,
            **self.build_time_filters(date_field="date_creation")
        ).order_by("-supporter_count")[:50]

    def get_fallacy_premises(self):
        return Premise.objects.annotate(
            report_count=Sum("reports"),
        ).filter(
            argument__community=self.request.community,
            report_count__gt=0,
            **self.build_time_filters(date_field="date_creation")
        ).order_by("-report_count")[:10]

    def get_crowded_contentions(self):
        return Contention.objects.annotate(
            premise_count=Sum("premises"),
        ).filter(
            community=self.request.community,
            language=normalize_language_code(get_language()),
            premise_count__gt=0,
            **self.build_time_filters(date_field="date_creation")
        ).order_by("-premise_count")[:10]


class UpdatedArgumentsView(HomeView):
    tab_class = "updated"

    def get_contentions(self, paginate=True):
        contentions = (Contention
                       .objects
                       .filter(is_published=True)
                       .order_by('-date_modification'))

        contentions = self.apply_community_filter(contentions)

        if paginate:
            contentions = contentions[self.get_offset():self.get_limit()]

        return contentions


class ControversialArgumentsView(HomeView):
    tab_class = "controversial"

    def get_contentions(self, paginate=True):
        last_week = now() - timedelta(days=3)
        contentions = (Contention
                       .objects
                       .annotate(num_children=Count('premises'))
                       .order_by('-num_children')
                       .filter(date_modification__gte=last_week))

        contentions = self.apply_community_filter(contentions)

        if paginate:
            return contentions[self.get_offset():self.get_limit()]

        return contentions


class AboutView(TemplateView):
    template_name = "about.html"

    def get_text_file(self):
        language = get_language()

        if self.request.community:
            return self.request.community.about

        return render_to_string("about-%s.md" % language)

    def get_context_data(self, **kwargs):
        content = markdown(self.get_text_file())
        return super(AboutView, self).get_context_data(
            content=content, **kwargs)


class TosView(TemplateView):
    template_name = "tos.html"

    def get_text_file(self):
        if self.request.community:
            return self.request.community.about

        return render_to_string("tos.md")

    def get_context_data(self, **kwargs):
        content = markdown(self.get_text_file())
        return super(TosView, self).get_context_data(
            content=content, **kwargs)


class ArgumentCreationView(LoginRequiredMixin, CreateView):
    template_name = "premises/new_contention.html"
    form_class = ArgumentCreationForm

    help_texts = {
        'title': 'premises/examples/contention.html',
        'owner': 'premises/examples/owner.html',
        'sources': 'premises/examples/sources.html'
    }

    def get_form_class(self):
        form_class = self.form_class
        for key, value in self.help_texts.items():
            help_text = render_to_string(value)
            form_class.base_fields[key].help_text = help_text
        return form_class

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.ip_address = get_ip_address(self.request)
        form.instance.language = normalize_language_code(get_language())
        form.instance.is_published = True
        response = super(ArgumentCreationView, self).form_valid(form)
        form.instance.update_sibling_counts()
        form.instance.save_nouns()
        form.instance.save()
        return response


class ArgumentUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "premises/edit_contention.html"
    form_class = ArgumentCreationForm

    def get_queryset(self):
        contentions = Contention.objects.all()
        if self.request.user.is_superuser:
            return contentions
        return contentions.filter(user=self.request.user)

    def form_valid(self, form):
        response = super(ArgumentUpdateView, self).form_valid(form)
        form.instance.update_sibling_counts()
        form.instance.nouns.clear()
        form.instance.save_nouns()
        form.instance.save()
        return response


class ArgumentPublishView(LoginRequiredMixin, DetailView):
    def get_queryset(self):
        return Contention.objects.filter(user=self.request.user)

    def post(self, request, slug):
        contention = self.get_object()
        contention.is_published = True
        contention.save()
        messages.info(request, u"Argument is published now.")
        return redirect(contention)


class ArgumentUnpublishView(LoginRequiredMixin, DetailView):
    def get_queryset(self):
        return Contention.objects.filter(user=self.request.user)

    def post(self, request, slug):
        contention = self.get_object()
        contention.is_published = False
        contention.save()
        messages.info(request, u"Argüman yayından kaldırıldı.")
        return redirect(contention)


class ArgumentDeleteView(LoginRequiredMixin, DetailView):
    def get_queryset(self):
        return Contention.objects.filter(user=self.request.user)

    def post(self, request, slug):
        contention = self.get_object()
        if check_content_deletion(contention):
            # remove notification
            Entry.objects.delete(contention.get_newsfeed_type(), contention.id)
            contention.delete()
            messages.info(request, u"Argument has been removed.")
            return redirect("home")
        else:
            messages.info(request, u"Argument cannot be deleted.")
            return redirect(contention)

    delete = post


class PremiseEditView(LoginRequiredMixin, UpdateView):
    template_name = "premises/edit_premise.html"
    form_class = PremiseEditForm

    help_texts = {
        'premise_type': 'premises/examples/premise_type.html',
        'text': 'premises/examples/premise.html',
        'sources': 'premises/examples/premise_source.html'
    }

    def get_form_class(self):
        form_class = self.form_class
        for key, value in self.help_texts.items():
            help_text = render_to_string(value)
            form_class.base_fields[key].help_text = help_text
        return form_class

    def get_queryset(self):
        premises = Premise.objects.all()
        if self.request.user.is_superuser:
            return premises
        return premises.filter(user=self.request.user)

    def form_valid(self, form):
        response = super(PremiseEditView, self).form_valid(form)
        form.instance.argument.update_sibling_counts()
        return response

    def get_context_data(self, **kwargs):
        return super(PremiseEditView, self).get_context_data(**kwargs)


class PremiseCreationView(NextURLMixin, LoginRequiredMixin, CreateView):
    template_name = "premises/new_premise.html"
    form_class = PremiseCreationForm

    help_texts = {
        'premise_type': 'premises/examples/premise_type.html',
        'text': 'premises/examples/premise.html',
        'sources': 'premises/examples/premise_source.html'
    }

    def get_form_class(self):
        form_class = self.form_class
        for key, value in self.help_texts.items():
            help_text = render_to_string(value)
            form_class.base_fields[key].help_text = help_text
        return form_class

    def get_context_data(self, **kwargs):
        return super(PremiseCreationView, self).get_context_data(
            contention=self.get_contention(),
            view=self.get_view_name(),
            parent=self.get_parent(),
            **kwargs)

    def form_valid(self, form):
        contention = self.get_contention()
        form.instance.user = self.request.user
        form.instance.argument = contention
        form.instance.parent = self.get_parent()
        form.instance.is_approved = True
        form.instance.ip_address = get_ip_address(self.request)
        form.save()
        contention.update_sibling_counts()

        if form.instance.parent:
            added_premise_for_premise.send(sender=self,
                                           premise=form.instance)
        else:
            added_premise_for_contention.send(sender=self,
                                              premise=form.instance)

        contention.date_modification = timezone.now()
        contention.update_premise_weights()
        contention.save()

        return redirect(
            form.instance.get_parent().get_absolute_url() +
            self.get_next_parameter()
        )

    def get_contention(self):
        return get_object_or_404(Contention, slug=self.kwargs['slug'])

    def get_parent(self):
        parent_pk = self.kwargs.get("pk")
        if parent_pk:
            return get_object_or_404(Premise, pk=parent_pk)


class PremiseSupportView(NextURLMixin, LoginRequiredMixin, View):
    def get_premise(self):
        premises = Premise.objects.exclude(user=self.request.user)
        return get_object_or_404(premises, pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        premise = self.get_premise()
        premise.supporters.add(self.request.user)
        supported_a_premise.send(sender=self, premise=premise,
                                 user=self.request.user)
        premise.argument.update_premise_weights()

        if request.is_ajax():
            return HttpResponse(status=201)

        return redirect(
            premise.get_parent().get_absolute_url() +
            self.get_next_parameter() +
            "#%s" % premise.pk
        )

    def get_contention(self):
        return get_object_or_404(Contention, slug=self.kwargs['slug'])


class PremiseUnsupportView(PremiseSupportView):
    def delete(self, request, *args, **kwargs):
        premise = self.get_premise()
        premise.supporters.remove(self.request.user)
        premise.argument.update_premise_weights()

        if request.is_ajax():
            return HttpResponse(status=204)

        return redirect(
            premise.get_parent().get_absolute_url() +
            self.get_next_parameter() + 
            "#%s" % premise.pk
        )

    post = delete


class PremiseDeleteView(LoginRequiredMixin, View):
    def get_premise(self):
        if self.request.user.is_staff:
            premises = Premise.objects.all()
        else:
            premises = Premise.objects.filter(user=self.request.user)
        return get_object_or_404(premises,
                                 pk=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        premise = self.get_premise()
        premise.delete()
        premise.update_sibling_counts()
        contention = self.get_contention()
        if not contention.premises.exists():
            contention.is_published = False
            contention.save()
        contention.update_premise_weights()
        return redirect(contention)

    post = delete

    def get_contention(self):
        return get_object_or_404(Contention, slug=self.kwargs['slug'])


class ReportView(NextURLMixin, LoginRequiredMixin, CreateView):
    form_class = ReportForm
    template_name = "premises/report.html"

    def get_form_class(self):
        form = self.form_class
        help_text = render_to_string('premises/examples/fallacy.html')
        form.base_fields['fallacy_type'].help_text = help_text
        return form

    def get_context_data(self, **kwargs):
        return super(ReportView, self).get_context_data(
            premise=self.get_premise(),
            view=self.get_view_name(),
            **kwargs)

    def get_contention(self):
        return get_object_or_404(Contention, slug=self.kwargs['slug'])

    def get_premise(self):
        return get_object_or_404(Premise, pk=self.kwargs['pk'])

    def get_initial(self):
        return {
            'contention': self.get_contention(),
            'premise': self.get_premise(),
            'reporter': self.request.user
        }

    def form_valid(self, form):
        contention = self.get_contention()
        premise = self.get_premise()
        form.instance.contention = contention
        form.instance.premise = premise
        form.instance.reporter = self.request.user
        form.save()
        reported_as_fallacy.send(sender=self, report=form.instance)
        contention.update_premise_weights()
        return redirect(
            premise.get_parent().get_absolute_url() +
            self.get_next_parameter() +
            "#%s" % premise.pk
        )


class RemoveReportView(NextURLMixin, LoginRequiredMixin, View):
    def get_premise(self):
        return get_object_or_404(Premise, pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        premise = self.get_premise()
        premise.reports.filter(
            reporter=request.user,
            fallacy_type=request.GET.get('type')
        ).delete()
        return redirect(
            premise.get_parent().get_absolute_url() +
            self.get_next_parameter() +
            "#%s" % premise.pk
        )
