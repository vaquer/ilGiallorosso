# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20160110_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='date',
            field=models.DateField(default=datetime.datetime(2016, 1, 13, 19, 20, 32, 498407, tzinfo=utc), verbose_name=b'Fecha de Publicacion', db_index=True),
        ),
    ]
