# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('notification_type', models.IntegerField(choices=[(0, b'added-premise-for-contention'), (1, b'added-premise-for-premise'), (2, b'reported-as-fallacy'), (3, b'followed')])),
                ('is_read', models.BooleanField(default=False)),
                ('target_object_id', models.IntegerField(null=True, blank=True)),
                ('recipient', models.ForeignKey(related_name=b'notifications', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(related_name=b'sent_notifications', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['is_read', '-date_created'],
            },
            bases=(models.Model,),
        ),
    ]
