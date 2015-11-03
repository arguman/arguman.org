# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nouns', '0011_auto_20151102_2154'),
    ]

    operations = [
        migrations.RenameModel('Synonym', 'Keyword')
    ]
