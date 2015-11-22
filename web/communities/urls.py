from django.conf.urls import patterns, url

from communities.views import MembershipConfirmation

urlpatterns = patterns(
    '',
    url(r'^confirm$', MembershipConfirmation.as_view(), name='community_membership_confirm'),
)
