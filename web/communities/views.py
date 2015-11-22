from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from profiles.mixins import LoginRequiredMixin


class MembershipConfirmation(LoginRequiredMixin, TemplateView):
    def get(self, request):
        if not request.community:
            return HttpResponse(status=400)

        if request.community.get_membership(request.user):
            return HttpResponse(status=301)

        return render(request, 'communities/confirm.html')

    def post(self, request):
        request.community.add_member(request.user)
        return redirect(reverse("home"))
