# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('premises', '0007_auto_20141020_2215'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contention', models.ForeignKey(related_name=b'contention_report', blank=True, to='premises.Contention', null=True)),
                ('premise', models.ForeignKey(related_name=b'comment_report', blank=True, to='premises.Premise', null=True)),
                ('reporter', models.ForeignKey(related_name=b'reporter', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name=b'user_report', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
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
