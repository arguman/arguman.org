# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0021_auto_20141107_0059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contention',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='report',
            name='fallacy_type',
            field=models.CharField(default=b'Wrong Direction', choices=[['Begging The Question,', 'K\u0131s\u0131r D\xf6ng\xfc Safsatas\u0131'], ['Irrelevant Conclusion', 'Alakas\u0131z Sonu\xe7 Safsatas\u0131'], ['Fallacy of Irrelevant Purpose', 'Alakas\u0131z Ama\xe7 Safsatas\u0131'], ['Fallacy of Red Herring', 'Konuyu Sapt\u0131rma Safsatas\u0131'], ['Argument Against the Man', 'Adam Karalama Safsatas\u0131'], ['Poisoning The Well', 'Dolduru\u015fa Getirme Safsatas\u0131'], ['Fallacy Of The Beard', 'Devede Kulak Safsatas\u0131'], ['Fallacy of Slippery Slope', 'Felaket Tellall\u0131\u011f\u0131 Safsatas\u0131'], ['Fallacy of False Cause', 'Yanl\u0131\u015f Sebep Safsatas\u0131'], ['Fallacy of \u201cPrevious This\u201d', '\xd6ncesinde Safsatas\u0131'], ['Joint Effect', 'M\xfc\u015fterek Etki'], ['Wrong Direction', 'Yanl\u0131\u015f Y\xf6n Safsatas\u0131'], ['False Analogy', 'Yanl\u0131\u015f Benzetme Safsatas\u0131'], ['Slothful Induction', 'Yok Sayma Safsatas\u0131'], ['Appeal to Belief', '\u0130nanca Ba\u015fvurma Safsatas\u0131'], ['Pragmatic Fallacy', 'Faydac\u0131 Safsata'], ['Fallacy Of \u201c\u0130s\u201d To \u201cOught\u201d', 'Dayatma Safsatas\u0131'], ['Argument From Force', 'Tehdit Safsatas\u0131'], ['Argument To Pity', 'Duygu S\xf6m\xfcr\xfcs\xfc'], ['Prejudicial Language', '\xd6nyarg\u0131l\u0131 Dil Safsatas\u0131'], ['Fallacy Of Special Pleading', 'Mazeret Safsatas\u0131'], ['Appeal To Authority', 'Bir Bilen Safsatas\u0131']], max_length=255, help_text='Safsata tipi belirtilmesi gereklidir. Bunlar hakk\u0131nda daha fazla\nbilgi i\xe7in <a href="http://safsatakilavuzu.com">safsatakilavuzu.com</a> adresini\nziyaret edebilirsiniz.', null=True, verbose_name=b'Safsata Tipi'),
        ),
    ]
