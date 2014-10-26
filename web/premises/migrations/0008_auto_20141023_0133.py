# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0007_auto_20141020_2215'),
    ]

    operations = [
        migrations.AddField(
            model_name='contention',
            name='date_modification',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 23, 1, 33, 8, 359184), auto_now=True, auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='premise',
            name='is_approved',
            field=models.BooleanField(default=False, verbose_name=b'Yay\xc4\xb1nla'),
        ),
        migrations.AlterField(
            model_name='premise',
            name='parent',
            field=models.ForeignKey(related_name=b'children', blank=True, to='premises.Premise', help_text=b'\xc3\x96nermenin \xc3\xb6nc\xc3\xbcl\xc3\xbc. E\xc4\x9fer bo\xc5\x9f b\xc4\xb1rak\xc4\xb1l\xc4\xb1rsaana arg\xc3\xbcman\xc4\xb1n bir \xc3\xb6nermesi olur.', null=True, verbose_name=b'\xc3\x96nc\xc3\xbcl\xc3\xbc'),
        ),
    ]
