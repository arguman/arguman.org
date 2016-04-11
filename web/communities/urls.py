from django.conf.urls import patterns, url

from communities.views import MembershipConfirmation, MembershipList

urlpatterns = patterns(
    '',
    url(r'^confirm$', MembershipConfirmation.as_view(), name='community_membership_confirm'),
    url(r'^memberships$', MembershipList.as_view(), name='community_memberships'),
)
