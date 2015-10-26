from django.core.management import BaseCommand

from premises.models import Contention, Premise, Report


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        reports = (Report.objects
         .filter(contention__language='en'))

        fallacies = []

        for report in reports:
        	if report.report_type and report.premise:
        		fallacies.append({
        			"premise": report.premise.text,
        			"premise_type": report.premise.premise_class(),
        			"fallacy_type": report.fallacy_type
        		})

        json.dump(open('fallacies.json', 'w'))
