from functools import partial

from django.utils.safestring import mark_safe


def int_or_default(value, default=None):
    try:
        return abs(int(value))
    except (ValueError, TypeError):
        return default


int_or_zero = partial(int_or_default, default=0)


def wrap_tag(text, link, tag='a'):
    template = '<%(tag)s %(attr)s="%(link)s">%(text)s</%(tag)s>'
    attr = 'href' if tag == 'a' else 'data-href'
    return mark_safe(template % {
        'tag': tag,
        'text': text,
        'link': link,
        'attr': attr
    })


def replace_with_link(source, text, url, tag):
    lower_source = source.lower()
    text = text.lower()

    if text not in lower_source:
        return

    position = lower_source.index(text)

    left = source[:position]
    middle = source[position:position + len(text)]
    right = source[position + len(text):]

    token_start, token_end = '<' + tag, '</' + tag
    if (left.count(token_start) !=
            left.count(token_end)):
        return

    link = (left +
            wrap_tag(middle, url, tag) +
            right)

    return link
