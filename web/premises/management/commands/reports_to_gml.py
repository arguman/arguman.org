from django.core.management import BaseCommand
from unidecode import unidecode

from premises.models import Report, get_fallacy_types, Premise, Contention

import networkx as nx

graph = nx.Graph()


class Command(BaseCommand):

    def normalize(self, value):
        return (value
                .replace('"', '')
                .rstrip(","))

    def handle(self, *args, **kwargs):
        self.create_conjunction_graph()


    def create_conjunction_graph(self):
        fallacy_map = {
            unidecode(key): value
            for (key, value) in
            get_fallacy_types()
        }
        for contention in Contention.objects.all():
            for premise in contention.premises.all():
                fallacies = filter(None, premise.reports.values_list(
                    'fallacy_type', flat=True))
                fallacies = [
                    fallacy_map[unidecode(_f)]
                    for _f in fallacies
                ]
                fallacies_set = set(fallacies)
                for fallacy in fallacies_set:
                    graph.add_edges_from(
                        [
                            (unidecode(self.normalize(fallacy)),
                             unidecode(self.normalize(_f)))
                            for _f in fallacies_set
                            if _f != fallacy
                        ]
                    )


        nx.write_gml(graph, 'conjunction.gml')


    def create_report_graph(self):
        for (fallacy_type, localized) in get_fallacy_types():
            node = unidecode(self.normalize(localized))

            graph.add_node(node, type="fallacy", Weight=10)

            for premise in Premise.objects.filter(
                    reports__fallacy_type=fallacy_type):

                graph.add_node(premise.argument.pk, type="argument")

                graph.add_edge(premise.argument.pk, node, type="reported")

                if premise.argument.channel:
                    channel_node = unidecode(premise.argument.channel.title)

                    graph.add_node(channel_node, type="channel",
                                   Weight=premise.argument.channel.contentions.count() * 30)
                    graph.add_edge(channel_node, node, type="reported")


        nx.write_gml(graph, 'reports.gml')
