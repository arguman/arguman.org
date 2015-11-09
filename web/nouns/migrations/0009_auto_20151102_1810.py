# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nouns', '0008_auto_20151031_2148'),
    ]

    operations = [
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('relation_type', models.CharField(max_length=25, choices=[(b'hypernym', b'Is a'), (b'meronym', b'Part of'), (b'antonym', b'Opposite with')])),
                ('is_active', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('from_noun', models.ForeignKey(related_name=b'from_relations', to='nouns.Noun')),
                ('to_noun', models.ForeignKey(related_name=b'to_relations', to='nouns.Noun')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='Pattern',
        ),
        migrations.RemoveField(
            model_name='noun',
            name='antonyms',
        ),
        migrations.RemoveField(
            model_name='noun',
            name='hypernyms',
        ),
        migrations.AddField(
            model_name='synonym',
            name='is_visible',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
