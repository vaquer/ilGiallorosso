# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20160114_0220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='date',
            field=models.DateField(default=datetime.datetime(2016, 1, 29, 5, 55, 12, 105342, tzinfo=utc), verbose_name=b'Fecha de Publicacion', db_index=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='tag',
            field=models.CharField(unique=True, max_length=150, verbose_name=b'Tag', db_index=True),
        ),
    ]
