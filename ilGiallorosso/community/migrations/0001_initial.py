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
            name='UserGiallorosso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('birth_date', models.DateField(verbose_name=b'Fecha de Nacimiento')),
                ('pic', models.ImageField(upload_to=b'users/pics', null=True, verbose_name=b'Imagen', blank=True)),
                ('social_media_user', models.BooleanField(default=False, verbose_name=b'Registrado por RedSocial')),
                ('active', models.BooleanField(default=False, verbose_name=b'Activo')),
                ('user', models.ForeignKey(verbose_name=b'Usuario Django', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
