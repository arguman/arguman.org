import json
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMultiAlternatives
import requests
from django.conf import settings


class PostmarkMessage(dict):

    def __init__(self, message, fail_silently=True):
        try:
            message_dict = {}
            message_dict["From"] = message.from_email
            message_dict["Subject"] = unicode(message.subject)
            message_dict["TextBody"] = unicode(message.body)

            if message.to:
                message_dict["To"] = ",".join(message.to)

            if message.cc:
                message_dict["Cc"] = ",".join(message.cc)

            if message.bcc:
                message_dict["Bcc"] = ",".join(message.bcc)

            if isinstance(message, EmailMultiAlternatives):
                    for alt in message.alternatives:
                        if alt[1] == "text/html":
                            message_dict["HtmlBody"] = unicode(alt[0])

            if len(message.extra_headers):
                message_dict["Headers"] = [{"Name": x[0], "Value": x[1]} for x in message.extra_headers.items()]
            if message.attachments and isinstance(message.attachments, list):
                if len(message.attachments):
                    message_dict["Attachments"] = message.attachments

        except:
            if fail_silently:
                message_dict = {}
            else:
                raise
        super(PostmarkMessage, self).__init__(message_dict)

class EmailBackend(BaseEmailBackend):

    def send_messages(self, email_messages):
        if not email_messages:
            return

        num_sent = 0
        try:
            for message in email_messages:
                sent = self._send(PostmarkMessage(message, self.fail_silently))
                if sent:
                    num_sent += 1
        except:
            if self.fail_silently:
                pass
            else:
                raise

        return num_sent


    def _send(self, message):

        requests.post(settings.POSTMARK_API_URL,
                      data=json.dumps(message),
                      headers={
                          "Accept": "application/json",
                          "Content-Type": "application/json",
                          "X-Postmark-Server-Token": settings.POSTMARK_TOKEN
                      })
