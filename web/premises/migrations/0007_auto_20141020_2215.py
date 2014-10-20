# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0006_contention_is_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='premise',
            name='sibling_count',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contention',
            name='description',
            field=models.TextField(null=True, verbose_name=b'Ek bilgiler', blank=True),
        ),
        migrations.AlterField(
            model_name='contention',
            name='owner',
            field=models.CharField(help_text='Arg\xfcman\u0131n sahibi. Bir kurum, kitap ya da ki\u015fi olabilir.\n\xd6rnekler:\n<ul>\n    <li>T.C. Anayasas\u0131</li>\n    <li>T\xfcrk Dil Kurumu</li>\n    <li>Friedrich Nietzsche</li>\n    <li>Piet Mondiran</li>\n    <li>Aziz Nesin</li>\n</ul>\nE\u011fer bir de\u011fer girilmemi\u015fse arg\xfcman\u0131n sahibi arg\xfcman\u0131 ekleyen olarak g\xf6r\xfcl\xfcr.', max_length=255, null=True, verbose_name=b'Orijinal s\xc3\xb6ylem', blank=True),
        ),
        migrations.AlterField(
            model_name='contention',
            name='sources',
            field=models.TextField(help_text='Arg\xfcman\u0131n kayna\u011f\u0131. Bir URL, kitap ad\u0131 ya da dergi ad\u0131 olabilir.\nBu alan \xf6nemlidir, kaynaks\u0131z ve tart\u0131\u015fmal\u0131 bir arg\xfcman/\xf6nerme yay\u0131ndan kald\u0131r\u0131l\u0131r.', null=True, verbose_name=b'Kaynaklar', blank=True),
        ),
        migrations.AlterField(
            model_name='contention',
            name='title',
            field=models.CharField(help_text="\xd6nermeleriyle birlikte tart\u0131\u015f\u0131labilecek, desteklenebilecek/ispatlanabilecek ya da \xe7\xfcr\xfct\xfclebilecek bir arg\xfcman.\n\xd6rnekler:\n<ul>\n    <li>Sanat toplum i\xe7indir.</li>\n    <li>Bisiklet bir ula\u015f\u0131m arac\u0131d\u0131r.</li>\n    <li>Bisiklet\xe7iler trafikte bulundu\u011fu t\xfcm \u015feridi kaplamal\u0131d\u0131r.</li>\n    <li>Python'\u0131n ilerlemesinde GIL b\xfcy\xfck bir engeldir.</li>\n</ul>", max_length=255, verbose_name=b'Arg\xc3\xbcman'),
        ),
        migrations.AlterField(
            model_name='premise',
            name='premise_type',
            field=models.IntegerField(default=1, help_text='\xd6nermenin tipi belirtilmesi gerekir. De\u011ferler \u015funlard\u0131r:\n<ul>\n    <li>\n        ama: itiraz ve \xe7\xfcr\xfctme i\xe7in kullan\u0131l\u0131r\n    </li>\n    <li>\n        \xe7\xfcnk\xfc: destek/kan\u0131t i\xe7in kullan\u0131l\u0131r\n    </li>\n    <li>\n        ancak: bir \xf6nermeye ek bilgi ya da durum belirtilmesi i\xe7in kullan\u0131l\u0131r.\n    </li>\n</ul>', verbose_name=b'\xc3\x96nerme Tipi', choices=[(0, 'ama'), (1, '\xe7\xfcnk\xfc'), (2, 'ancak')]),
        ),
        migrations.AlterField(
            model_name='premise',
            name='sources',
            field=models.TextField(help_text='\xd6rnek: T.C. Karayollar\u0131 Trafik Kanunu 2918/46. Maddesi', null=True, verbose_name=b'Kaynaklar', blank=True),
        ),
        migrations.AlterField(
            model_name='premise',
            name='text',
            field=models.TextField(help_text='\xd6rnek: Bisiklet s\xfcr\xfcc\xfcs\xfc karayolunda en sa\u011f \u015feridi kullan\u0131r ve di\u011fer ta\u015f\u0131tlar ile ayn\u0131 sorumlulukla hareket eder.', null=True, verbose_name=b'\xc3\x96nermenin \xc4\xb0\xc3\xa7eri\xc4\x9fi', blank=True),
        ),
    ]
