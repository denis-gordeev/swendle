# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-06-23 00:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20170623_0022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='grammar',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='hotness',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=b''),
        ),
        migrations.AlterField(
            model_name='article',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='party_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Party'),
        ),
        migrations.AlterField(
            model_name='article',
            name='party_subjectivity_article',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='spelling',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='story_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Story'),
        ),
        migrations.AlterField(
            model_name='article',
            name='subjectivity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='videos',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='source',
            name='source_subjectivity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='story',
            name='hotness',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='story',
            name='rating_subjectivity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='story',
            name='rating_users',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]