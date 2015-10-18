import json
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.functional import SimpleLazyObject
from pymongo import Connection
import requests

_connection = None

from django.core.mail import EmailMultiAlternatives

from django.template import Context

def send_complex_mail(subject, template_txt, template_html, _from, to, context):

    subject, from_email = subject, _from
    context['BASE_URL'] = settings.BASE_DOMAIN
    text_content = render_to_string(template_txt, Context(context))
    html_content = render_to_string(template_html, Context(context))
    headers =  {"X-Postmark-Server-Token": settings.POSTMARK_TOKEN,
                "Content-Type": "application/json",
                "Accept": "application/json"}

    data = {'From': _from,
            'To': (',').join(to),
            'Subject': subject,
            'TextBody': text_content,
            'HtmlBody': html_content,
            }
    response = requests.post(settings.POSTMARK_API_URL,
                  data=json.dumps(data),
                  headers=headers)

def get_connection():
    global _connection
    if not _connection:
        _connection = Connection(
            host=getattr(settings, 'MONGODB_HOST', None),
            port=getattr(settings, 'MONGODB_PORT', None)
        )
        username = getattr(settings, 'MONGODB_USERNAME', None)
        password = getattr(settings, 'MONGODB_PASSWORD', None)
        db = _connection[settings.MONGODB_DATABASE]
        if username and password:
            db.authenticate(username, password)
        return db
    return _connection[settings.MONGODB_DATABASE]


connection = SimpleLazyObject(get_connection)


def get_collection(collection_name):
    return getattr(connection, collection_name)
