# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0022_auto_20141112_1823'),
    ]

    operations = [
        migrations.AddField(
            model_name='contention',
            name='language',
            field=models.CharField(max_length=5, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contention',
            name='description',
            field=models.TextField(null=True, verbose_name='Description', blank=True),
        ),
        migrations.AlterField(
            model_name='contention',
            name='owner',
            field=models.CharField(help_text='\nThe owner of argument. It can be instutation, person, book, or a paper. Examples: <ul> <li>On the Origin of Species</li> <li>Friedrich Nietzsche</li> <li>Piet Mondiran</li> <li>The Guardian</li> </ul>', max_length=255, null=True, verbose_name='Original Discourse', blank=True),
        ),
        migrations.AlterField(
            model_name='contention',
            name='sources',
            field=models.TextField(help_text='\nThe source of argument. It can be a URL, a book, or a newspaper. It is important for reliability of main contention.\n', null=True, verbose_name='Sources', blank=True),
        ),
        migrations.AlterField(
            model_name='contention',
            name='title',
            field=models.CharField(help_text='\nThe main contention. It will be arguable with own premises. The Premises can prove or rebuttal this contention.<br> Examples: <ul> <li>Real art is for society, not for profit</li> <li>The meaning of life is 42</li> <li>Ethics man did what had to be done</li> </ul>', max_length=255, verbose_name='Argument'),
        ),
        migrations.AlterField(
            model_name='premise',
            name='is_approved',
            field=models.BooleanField(default=True, verbose_name='Published'),
        ),
        migrations.AlterField(
            model_name='premise',
            name='parent',
            field=models.ForeignKey(related_name=b'children', blank=True, to='premises.Premise', help_text="The parent of premise. If you don't choose anything, it will be a main premise.", null=True, verbose_name='Parent'),
        ),
        migrations.AlterField(
            model_name='premise',
            name='premise_type',
            field=models.IntegerField(default=1, help_text='\n\nThe type of premise. It can be: <ul> <li> but: An objection against the contention. </li> <li> because: A reason for proof the contention. </li> <li> however: An additional situation for the premise. </li> </ul>', verbose_name='Premise Type', choices=[(0, b'but'), (1, b'because'), (2, b'however')]),
        ),
        migrations.AlterField(
            model_name='premise',
            name='sources',
            field=models.TextField(help_text="\nExample: Charles Darwin's The Origin of Species", null=True, verbose_name='Sources', blank=True),
        ),
        migrations.AlterField(
            model_name='premise',
            name='text',
            field=models.TextField(blank=True, help_text='\nExample: We define happiness as a state of well-being, starting with being alive instead of dead.', null=True, verbose_name='Premise Content', validators=[django.core.validators.MaxLengthValidator(300)]),
        ),
        migrations.AlterField(
            model_name='report',
            name='fallacy_type',
            field=models.CharField(default=b'Wrong Direction', choices=[(b'BeggingTheQuestion,', 'Begging The Question'), (b'IrrelevantConclusion', 'Irrelevant Conclusion'), (b'FallacyOfIrrelevantPurpose', 'Fallacy Of Irrelevant Purpose'), (b'FallacyOfRedHerring', 'Fallacy Of Red Herring'), (b'ArgumentAgainstTheMan', 'Argument Against TheMan'), (b'PoisoningTheWell', 'Poisoning The Well'), (b'FallacyOfTheBeard', 'Fallacy Of The Beard'), (b'FallacyOfSlipperySlope', 'Fallacy Of Slippery Slope'), (b'FallacyOfFalseCause', 'Fallacy Of False Cause'), (b'FallacyOfPreviousThis', 'Fallacy Of Previous This'), (b'JointEffect', 'Joint Effect'), (b'WrongDirection', 'Wrong Direction'), (b'FalseAnalogy', 'False Analogy'), (b'SlothfulInduction', 'Slothful Induction'), (b'AppealToBelief', 'Appeal To Belief'), (b'PragmaticFallacy', 'Pragmatic Fallacy'), (b'FallacyOfIsToOught', 'Fallacy Of Is To Ought'), (b'ArgumentFromForce', 'Argument From Force'), (b'ArgumentToPity', 'Argument To Pity'), (b'PrejudicialLanguage', 'Prejudicial Language'), (b'FallacyOfSpecialPleading', 'Fallacy Of Special Pleading'), (b'AppealToAuthority', 'Appeal To Authority')], max_length=255, help_text='\nYou have to choose a fallacy type. For more information, you can look at the <a href="https://en.wikipedia.org/wiki/List_of_fallacies">wikipedia entry</a> for fallacies.', null=True, verbose_name='Fallacy Type'),
        ),
    ]
