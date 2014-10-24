# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('premises', '0008_auto_20141023_0133'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('like', models.BooleanField(default=False, db_index=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('premise', models.ForeignKey(to='premises.Premise')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('date_created',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='premise',
            name='like_count',
            field=models.PositiveIntegerField(default=0, db_index=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='premise',
            name='unlike_count',
            field=models.PositiveIntegerField(default=0, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contention',
            name='title',
            field=models.CharField(help_text="\xd6nermeleriyle birlikte tart\u0131\u015f\u0131labilecek, desteklenebilecek, ispatlanabilecek ya da \xe7\xfcr\xfct\xfclebilecek bir arg\xfcman.\n\xd6rnekler:\n<ul>\n    <li>Sanat toplum i\xe7indir.</li>\n    <li>Bisiklet bir ula\u015f\u0131m arac\u0131d\u0131r.</li>\n    <li>Bisiklet\xe7iler trafikte bulundu\u011fu t\xfcm \u015feridi kaplamal\u0131d\u0131r.</li>\n    <li>Python'\u0131n ilerlemesinde GIL b\xfcy\xfck bir engeldir.</li>\n</ul>", max_length=255, verbose_name=b'Arg\xc3\xbcman'),
        ),
        migrations.AlterField(
            model_name='premise',
            name='text',
            field=models.TextField(blank=True, help_text='\xd6rnek: Bisiklet s\xfcr\xfcc\xfcs\xfc karayolunda en sa\u011f \u015feridi kullan\u0131r ve di\u011fer ta\u015f\u0131tlar ile ayn\u0131 sorumlulukla hareket eder.', null=True, verbose_name=b'\xc3\x96nermenin \xc4\xb0\xc3\xa7eri\xc4\x9fi', validators=[django.core.validators.MaxLengthValidator(300)]),
        ),
    ]
