from django.template.defaulttags import register
from premises.models import get_fallacy_types
from django.conf import settings
from django.utils import timezone


@register.filter
def humanize_fallacy_type(value):
    return dict(get_fallacy_types()).get(value)


@register.filter
def check_content_deletion(contention):
    content_deletion = settings.CONTENT_DELETION
    last_deletion_date = contention.date_creation + content_deletion['LAST_DELETION_DATE']
    if not contention.premises.exists() and content_deletion['HAS_EMPTY_CONTENT_DELETION']:
        return True
    if contention.premises.count() <= content_deletion['MAX_PREMISE_COUNT'] and last_deletion_date > timezone.now():
        return True
    return False
