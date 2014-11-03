from django.dispatch import Signal

added_premise_for_contention = Signal(providing_args=["premise"])
added_premise_for_premise = Signal(providing_args=["premise"])
reported_as_fallacy = Signal(providing_args=["report"])
supported_a_premise = Signal(providing_args=["premise", "user"])
