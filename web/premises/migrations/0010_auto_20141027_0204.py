# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0009_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='user',
        ),
        migrations.AlterField(
            model_name='contention',
            name='is_published',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='contention',
            name='title',
            field=models.CharField(help_text="\xd6nermeleriyle birlikte tart\u0131\u015f\u0131labilecek, desteklenebilecek, ispatlanabilecek ya da \xe7\xfcr\xfct\xfclebilecek bir arg\xfcman.\n\xd6rnekler:\n<ul>\n    <li>Sanat toplum i\xe7indir.</li>\n    <li>Bisiklet bir ula\u015f\u0131m arac\u0131d\u0131r.</li>\n    <li>Bisiklet\xe7iler trafikte bulundu\u011fu t\xfcm \u015feridi kaplamal\u0131d\u0131r.</li>\n    <li>Python'\u0131n ilerlemesinde GIL b\xfcy\xfck bir engeldir.</li>\n</ul>", max_length=255, verbose_name=b'Arg\xc3\xbcman'),
        ),
        migrations.AlterField(
            model_name='premise',
            name='is_approved',
            field=models.BooleanField(default=True, verbose_name=b'Yay\xc4\xb1nla'),
        ),
        migrations.AlterField(
            model_name='premise',
            name='text',
            field=models.TextField(blank=True, help_text='\xd6rnek: Bisiklet s\xfcr\xfcc\xfcs\xfc karayolunda en sa\u011f \u015feridi kullan\u0131r ve di\u011fer ta\u015f\u0131tlar ile ayn\u0131 sorumlulukla hareket eder.', null=True, verbose_name=b'\xc3\x96nermenin \xc4\xb0\xc3\xa7eri\xc4\x9fi', validators=[django.core.validators.MaxLengthValidator(300)]),
        ),
        migrations.AlterField(
            model_name='report',
            name='contention',
            field=models.ForeignKey(related_name=b'reports', blank=True, to='premises.Contention', null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='premise',
            field=models.ForeignKey(related_name=b'reports', blank=True, to='premises.Premise', null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='reporter',
            field=models.ForeignKey(related_name=b'reports', to=settings.AUTH_USER_MODEL),
        ),
    ]
