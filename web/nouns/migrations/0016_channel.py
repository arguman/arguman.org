# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nouns', '0015_auto_20151104_2059'),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.CharField(max_length=255)),
                ('order', models.IntegerField()),
                ('nouns', models.ManyToManyField(to='nouns.Noun', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
