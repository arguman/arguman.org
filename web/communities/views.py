from communities.mixins import CommunityMixin
from communities.models import Membership
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from profiles.mixins import LoginRequiredMixin


class MembershipConfirmation(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        if not request.community:
            return HttpResponse(status=400)

        if request.community.get_membership(request.user):
            return HttpResponse(status=301)

        return render(request, 'communities/confirm.html')

    def post(self, request):
        request.community.add_member(request.user)
        return redirect(reverse("home"))


class MembershipList(CommunityMixin, TemplateView):
    # tab_class = 'search'
    template_name = 'communities/memberships.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user in request.community.owners:
            return HttpResponse(status=403)
        else:
            return super(MembershipList, self).dispatch(request, *args, **kwargs)



    def get_context_data(self, **kwargs):
        memberships = self.request.community.memberships.all()
        return super(MembershipList, self).get_context_data(
            memberships=memberships)

    def post(self, request):
        #FOR CHANGING MEMBERSHIP
        membership_id = request.POST.get('membership_id')
        membership = get_object_or_404(Membership, id=membership_id)
        if request.user in membership.community.owners:
            membership.change_access(request.POST.get('type'))
        else:
            return HttpResponse(status=403)
        return HttpResponse()