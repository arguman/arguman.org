# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=255)),
                ('community_type', models.CharField(max_length=255, choices=[(b'public', 'Public'), (b'restricted', 'Restricted'), (b'private', 'Private')])),
                ('language', models.CharField(max_length=255)),
                ('about', models.TextField(null=True, blank=True)),
                ('terms_of_service', models.TextField(null=True, blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Communities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('hash', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_owner', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('can_create_argument', models.BooleanField(default=False)),
                ('can_create_premise', models.BooleanField(default=False)),
                ('community', models.ForeignKey(related_name=b'memberships', to='communities.Community')),
                ('user', models.ForeignKey(related_name=b'memberships', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='invitation',
            name='membership',
            field=models.ForeignKey(to='communities.Membership'),
            preserve_default=True,
        ),
    ]
