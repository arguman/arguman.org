from django.shortcuts import render
from communities.models import Community


class CommunityMixin(object):

    def get_community(self, subdomain):
        try:
            community = Community.objects.get(name=subdomain)
        except Community.DoesNotExist:
            community = None

        return community

    def apply_community_filter(self, queryset):
        community = self.request.community

        if community:
            return queryset.filter(community=community)

        return queryset

    def dispatch(self, request, *args, **kwargs):
        community = request.community

        if community.user_can_view(request.user):
            return super(CommunityMixin, self).dispatch(request, *args, **kwargs)

        return render('communities/requires_membership.html')
