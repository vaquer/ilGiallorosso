# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('community', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_about', models.TextField(verbose_name=b'Biografia')),
                ('photo', models.ImageField(upload_to=b'blog/authors/photos', null=True, verbose_name=b'Foto de editor', blank=True)),
                ('user', models.ForeignKey(verbose_name=b'Usuario editor', to='community.UserGiallorosso')),
            ],
            options={
                'verbose_name': 'Autor',
                'verbose_name_plural': 'Autores',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=150, verbose_name=b'Categoria')),
                ('slug', models.SlugField(max_length=200, verbose_name=b'Slug')),
                ('short_description', models.CharField(max_length=500, verbose_name=b'Descripcion')),
                ('pic', models.ImageField(upload_to=b'blog/categories/pics', null=True, verbose_name=b'Imagen', blank=True)),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
            },
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=300, verbose_name=b'Titulo', db_index=True)),
                ('slug', models.SlugField(max_length=350, verbose_name=b'Slug')),
                ('date', models.DateField(default=datetime.datetime(2015, 10, 26, 2, 44, 30, 883032, tzinfo=utc), verbose_name=b'Fecha de Publicacion', db_index=True)),
                ('text', models.TextField(null=True, verbose_name=b'Texto', blank=True)),
                ('about', models.CharField(max_length=300, null=True, verbose_name=b'Encabezado', blank=True)),
                ('photo', models.ImageField(upload_to=b'blog/entries/photos', null=True, verbose_name=b'Imagen', blank=True)),
                ('top', models.BooleanField(default=False, verbose_name=b'Titular')),
                ('active', models.BooleanField(default=False, verbose_name=b'Publicar')),
                ('author', models.ForeignKey(verbose_name=b'Autor', blank=True, to='blog.Author', null=True)),
                ('category', models.ForeignKey(verbose_name=b'Categoria', blank=True, to='blog.Category', null=True)),
            ],
            options={
                'verbose_name': 'Entrada',
                'verbose_name_plural': 'Entradas',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(unique=True, max_length=150, verbose_name=b'Tag')),
                ('slug', models.SlugField(unique=True, max_length=200, verbose_name=b'Slug')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.AddField(
            model_name='entry',
            name='tags',
            field=models.ManyToManyField(db_index=True, to='blog.Tag', null=True, verbose_name=b'Tags', blank=True),
        ),
    ]
