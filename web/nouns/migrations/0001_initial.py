# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Noun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, blank=True)),
                ('is_active', models.BooleanField(default=False)),
                ('hypernyms', models.ManyToManyField(related_name='hypernyms_rel_+', null=True, to='nouns.Noun', blank=True)),
                ('synonyms', models.ManyToManyField(related_name='synonyms_rel_+', null=True, to='nouns.Noun', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pattern',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('text', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
