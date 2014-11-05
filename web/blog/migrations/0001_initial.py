# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import markitup.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug')),
                ('content', markitup.fields.MarkupField(no_rendered_field=True, verbose_name='Content')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('is_published', models.BooleanField(default=True, verbose_name='Published')),
                ('_content_rendered', models.TextField(editable=False, blank=True)),
            ],
            options={
                'ordering': ('-date_created',),
            },
            bases=(models.Model,),
        ),
    ]
