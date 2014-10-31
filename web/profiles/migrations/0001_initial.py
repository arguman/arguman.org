# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('notification_type', models.IntegerField(choices=[(0, b'added-premise-for-contention'), (1, b'added-premise-for-premise'), (2, b'reported-as-fallacy'), (3, b'followed')])),
                ('recipient', models.ForeignKey(related_name=b'notifications', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(related_name=b'sent_notifications', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
