import json
from django.core.mail import EmailMultiAlternatives
import requests
from django.conf import settings
from django.template import Context
from django.template.loader import render_to_string


def send_complex_mail(subject,
                      template_txt,
                      template_html,
                      _from,
                      to=None,
                      cc=None,
                      bcc=None,
                      context=None):

    context = {} if not context else context
    subject, from_email = subject, _from
    context['BASE_URL'] = settings.BASE_DOMAIN
    text_content = render_to_string(template_txt, Context(context))
    html_content = render_to_string(template_html, Context(context))

    msg = EmailMultiAlternatives(subject,
                                 text_content,
                                 from_email,
                                 to=to,
                                 cc=cc,
                                 bcc=bcc)
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=True)