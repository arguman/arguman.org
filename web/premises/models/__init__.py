from django.utils.translation import ugettext_lazy as _


NEWS_CONTENT_COUNT = 50
UPDATED_CONTENT_COUNT = 50
FEATURED_CONTENT_COUNT = 50

MAX_PREMISE_CONTENT_LENGTH = 300

OBJECTION = 0
SUPPORT = 1
SITUATION = 2

PREMISE_TYPES = (
    (OBJECTION, _("but")),
    (SUPPORT, _("because")),
    (SITUATION, _("however")),
)

FALLACY_TYPES = (
    ("BeggingTheQuestion,", _("Begging The Question")),
    ("IrrelevantConclusion", _("Irrelevant Conclusion")),
    ("FallacyOfIrrelevantPurpose", _("Fallacy Of Irrelevant Purpose")),
    ("FallacyOfRedHerring", _("Fallacy Of Red Herring")),
    ("ArgumentAgainstTheMan", _("Argument Against TheMan")),
    ("PoisoningTheWell", _("Poisoning The Well")),
    ("FallacyOfTheBeard", _("Fallacy Of The Beard")),
    ("FallacyOfSlipperySlope", _("Fallacy Of Slippery Slope")),
    ("FallacyOfFalseCause", _("Fallacy Of False Cause")),
    ("FallacyOfPreviousThis", _("Fallacy Of Previous This")),
    ("JointEffect", _("Joint Effect")),
    ("WrongDirection", _("Wrong Direction")),
    ("FalseAnalogy", _("False Analogy")),
    ("SlothfulInduction", _("Slothful Induction")),
    ("AppealToBelief", _("Appeal To Belief")),
    ("PragmaticFallacy", _("Pragmatic Fallacy")),
    ("FallacyOfIsToOught", _("Fallacy Of Is To Ought")),
    ("ArgumentFromForce", _("Argument From Force")),
    ("ArgumentToPity", _("Argument To Pity")),
    ("PrejudicialLanguage", _("Prejudicial Language")),
    ("FallacyOfSpecialPleading", _("Fallacy Of Special Pleading")),
    ("AppealToAuthority", _("Appeal To Authority"))
)

from channel import Channel
from contention import Contention
from premise import Premise
from comment import Comment
from report import Report
