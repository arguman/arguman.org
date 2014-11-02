# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0015_premise_collapsed'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='fallacy_type',
            field=models.CharField(max_length=255, null=True, verbose_name=[['Serbest Safsatalar', '\u0130nformel fallacies'], ['Cinasl\u0131 Safsata', 'Fallacy of Equivocation'], ['\xc7ok Anlaml\u0131l\u0131k Safsatas\u0131', 'Fallacy of Amphiboly'], ['Vurgulama Safsatas\u0131', 'Fallacy of Accent'], ['\xd6zelle\u015ftirme Safsatas\u0131', 'Fallacy Of Accident'], ['Genelle\u015ftirme Safsatas\u0131', 'Fallacy of Converse Accident'], ['B\xfct\xfcnleme Safsatas\u0131', 'Fallacy of Composition'], ['\u0130ndirgeme Safsatas\u0131', 'Fallacy Of Division'], ['K\u0131s\u0131r D\xf6ng\xfc Safsatas\u0131', 'Begging The Question,'], ['Alakas\u0131z Sonu\xe7 Safsatas\u0131', 'Irrelevant Conclusion'], ['\u0130ddiay\u0131 Zay\u0131flatma Safsatas\u0131', 'Fallacy of the Straw-Man'], ['Alakas\u0131z Ama\xe7 Safsatas\u0131', 'Fallacy of \u0130rrelevant Purpose'], ['Konuyu Sapt\u0131rma Safsatas\u0131', 'Fallacy of Red Herring'], ['Adam Karalama Safsatas\u0131', 'Argument Against the Man'], ['Niteliksel Adam Karalama', 'Circumstantial Ad Hominem'], ['\u201cSen de\u201d Safsatas\u0131', 'Fallacy Of \u201cYou Also\u201d'], ['Dolduru\u015fa Getirme Safsatas\u0131', 'Poisoning The Well'], ['Devede Kulak Safsatas\u0131', 'Fallacy Of The Beard'], ['Ya Siyah Ya Beyaz Safsatas\u0131', 'Black And White Fallacy'], ['\u0130spatlama Mecburiyeti Safsatas\u0131', 'Argument From Ignorance'], ['Felaket Tellall\u0131\u011f\u0131 Safsatas\u0131', 'Fallacy of Slippery Slope'], ['\u0130mal\u0131 Soru Safsatas\u0131', 'Complex Question'], ['\xc7ok Sorulu Safsata', 'Fallacy Of Many Questions'], ['S\u0131n\u0131rl\u0131 Se\xe7enek Safsatas\u0131', 'Fallacy of Limited Alternatives'], ['Yanl\u0131\u015f Sebep Safsatas\u0131', 'Fallacy of False Cause'], ['\xd6ncesinde Safsatas\u0131', 'Fallacy of \u201cPrevious This\u201d'], ['M\xfc\u015fterek Etki', 'Joint Effect'], ['\u0130hmal Edilebilir Neden Safsatas\u0131', 'Genuine but Insignificant Cause'], ['Yanl\u0131\u015f Y\xf6n Safsatas\u0131', 'Wrong Direction,'], ['Karma\u015f\u0131k Nedenler Safsatas\u0131', 'Complex Cause'], ['Yetersiz \xd6rnek Safsatas\u0131', '(Fallacy of Insufficient Sample)'], ['Temsil Etmeyen \xd6rnek Safsatas\u0131', 'Unrepresentative Sample'], ['Yanl\u0131\u015f Benzetme Safsatas\u0131', 'False Analogy'], ['Yok Sayma Safsatas\u0131', 'Slothful Induction'], ['S\xfcmen Alt\u0131 Safsatas\u0131', 'Fallacy of Slanting'], ['Kumarbaz Safsatas\u0131', 'Gambler\u2019s Fallacy'], ['Bir Bilen Safsatas\u0131', 'Argument To Authority'], ['\u0130rrasyonel Otorite Safsatas\u0131', 'Fallacy Of Unqualified Source'], ['\u0130nanca Ba\u015fvurma Safsatas\u0131', 'Appeal to Belief'], ['Ortak Tutuma Ba\u015fvurma Safsatas\u0131', 'Appeal To Common Practice'], ['Grup Bask\u0131s\u0131 Safsatas\u0131', 'Bandwagon, Peer Pressure'], ['Faydac\u0131 Safsata', 'Pragmatic Fallacy'], ['Be\u011fendirme Safsatas\u0131', 'Appeal To Personal \u0130nterests'], ['Dayatma Safsatas\u0131', 'Fallacy Of \u201c\u0130s\u201d To \u201cOught\u201d'], ['Mazruf De\u011fil Zarf Safsatas\u0131', 'Style Over Substance'], ['Genetik Safsatas\u0131', 'Genetic Fallacy'], ['Tehdit Safsatas\u0131', 'Argument From Force'], ['Duygu S\xf6m\xfcr\xfcs\xfc', 'Argument To Pity'], ['\xd6nyarg\u0131l\u0131 Dil Safsatas\u0131', 'Prejudicial Language'], ['Mazeret Safsatas\u0131', 'Fallacy Of Special Pleading']]),
            preserve_default=True,
        ),
    ]
