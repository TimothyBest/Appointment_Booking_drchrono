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
            name='Doctor',
            fields=[
                ('id', models.CharField(max_length=255, unique=True, serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=255, null=True)),
                ('last_name', models.CharField(max_length=255, null=True)),
                ('suffix', models.CharField(max_length=255, null=True)),
                ('job_title', models.CharField(max_length=255, null=True)),
                ('specialty', models.CharField(max_length=255, null=True)),
                ('cell_phone', models.CharField(max_length=255, null=True)),
                ('home_phone', models.CharField(max_length=255, null=True)),
                ('office_phone', models.CharField(max_length=255, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('website', models.CharField(max_length=255, null=True)),
                ('user', models.ForeignKey(related_name='doctors', verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.CharField(max_length=255, unique=True, serialize=False, primary_key=True)),
                ('doctor', models.CharField(max_length=255, null=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('address', models.CharField(max_length=255, null=True)),
                ('city', models.CharField(max_length=255, null=True)),
                ('country', models.CharField(max_length=255, null=True)),
                ('state', models.CharField(max_length=255, null=True)),
                ('zip_code', models.CharField(max_length=255, null=True)),
                ('phone_number', models.CharField(max_length=255, null=True)),
                ('online_scheduling', models.CharField(max_length=255, null=True)),
                ('online_timeslots', models.CharField(max_length=255, null=True)),
                ('start_time', models.CharField(max_length=255, null=True)),
                ('end_time', models.CharField(max_length=255, null=True)),
                ('exam_rooms', models.CharField(max_length=255, null=True)),
                ('user', models.ForeignKey(related_name='offices', verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.CharField(max_length=255, unique=True, serialize=False, primary_key=True)),
                ('date_of_birth', models.DateField(null=True)),
                ('doctor', models.CharField(max_length=255, null=True)),
                ('first_name', models.CharField(max_length=255, null=True)),
                ('last_name', models.CharField(max_length=255, null=True)),
                ('cell_phone', models.CharField(max_length=255, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('state', models.CharField(max_length=2, null=True)),
                ('user', models.ForeignKey(related_name='patients', verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
