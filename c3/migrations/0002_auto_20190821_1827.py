# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        ('c3', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='talk',
            name='fahrplan_id',
        ),
        migrations.AddField(
            model_name='talk',
            name='c_persons',
            field=models.TextField(null=True, verbose_name='Persons'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='talk',
            name='c_tags',
            field=models.TextField(null=True, verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='talk',
            name='d_descriptions',
            field=models.TextField(null=True, verbose_name='Description'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='talk',
            name='d_names',
            field=models.TextField(null=True, verbose_name='Title'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='talk',
            name='d_subtitles',
            field=models.TextField(null=True, verbose_name='Subtitle'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='talk',
            name='description',
            field=models.TextField(null=True, verbose_name='Description'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='talk',
            name='fahrplan_guid',
            field=models.CharField(max_length=199, null=True, verbose_name=b'Fahrplan GUID'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='talk',
            name='i_language',
            field=models.PositiveIntegerField(default=0, verbose_name='Language', choices=[(0, 'English'), (1, 'German'), (2, 'Other')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='talk',
            name='length',
            field=models.PositiveIntegerField(null=True, verbose_name='Length'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='talk',
            name='subtitle',
            field=models.CharField(max_length=100, null=True, verbose_name='Subtitle'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='talk',
            name='url',
            field=models.URLField(null=True, verbose_name='About'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='talk',
            name='watch_url',
            field=models.URLField(null=True, verbose_name='Watch'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ccc',
            name='image',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'ccc'), max_length=500, verbose_name='Logo'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='talk',
            name='end_date',
            field=models.DateTimeField(null=True, verbose_name='End date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='talk',
            name='image',
            field=models.ImageField(max_length=500, null=True, verbose_name='Image', upload_to=magi.utils.uploadItem(b'talk')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='talk',
            name='start_date',
            field=models.DateTimeField(verbose_name='Start date'),
            preserve_default=True,
        ),
    ]
