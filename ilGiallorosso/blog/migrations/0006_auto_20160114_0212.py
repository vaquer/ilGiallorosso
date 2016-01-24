# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20160114_0208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='date',
            field=models.DateField(default=datetime.datetime(2016, 1, 14, 2, 12, 19, 498401, tzinfo=utc), verbose_name=b'Fecha de Publicacion', db_index=True),
        ),
    ]
