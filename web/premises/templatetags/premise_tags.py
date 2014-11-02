from django.template.defaulttags import register
from premises.models import get_fallacy_types


@register.filter
def humanize_fallacy_type(value):
    return dict(get_fallacy_types()).get(value)
