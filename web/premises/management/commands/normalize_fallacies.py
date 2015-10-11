# coding=utf-8
from django.core.management import BaseCommand

from premises.models import Report


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        reports = Report.objects.all()

        for report in reports:
            fallacy_type = report.fallacy_type or ""

            fallacy_type = (
                fallacy_type
                    .replace(' ', '')
                    .replace(u'İ', 'I')
                    .replace(u'“', '')
                    .replace(u'”', '')
                    .replace("of", "Of")
                    .replace("to", "To")
                    .replace("the", "The")
            )

            report.fallacy_type = fallacy_type
            report.save()
