from django.template.defaulttags import register
from django_gravatar.helpers import GRAVATAR_DEFAULT_SIZE, get_gravatar_url
from django.utils.html import escape
from django.conf import settings
from django.utils import timezone

from premises.models import FALLACY_TYPES


@register.filter
def humanize_fallacy_type(value):
    return dict(FALLACY_TYPES).get(value)


@register.filter
def check_content_deletion(contention):
    content_deletion = settings.CONTENT_DELETION
    last_deletion_date = contention.date_creation + content_deletion['LAST_DELETION_DATE']
    if not contention.premises.exists() and content_deletion['HAS_EMPTY_CONTENT_DELETION']:
        return True
    if contention.premises.count() <= content_deletion['MAX_PREMISE_COUNT'] and last_deletion_date > timezone.now():
        return True
    return False


@register.filter
def percentformat(value):
    return min(40, max(5, value))


def gravatar(user_or_email, size=GRAVATAR_DEFAULT_SIZE, alt_text='', css_class='gravatar'):
    """ Builds an gravatar <img> tag from an user or email """
    if hasattr(user_or_email, 'email'):
        email = user_or_email.email
    else:
        email = user_or_email

    try:
        url = escape(get_gravatar_url(email=email, size=size))
    except:
        return ''
    template = '<img class="{css_class}" src="{src}" width="{width}" height="{height}" alt="{alt}" />'
    return template.format(
        css_class=css_class, src=url, width=size, height=size, alt=alt_text)
