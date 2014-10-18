# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_email', models.EmailField(max_length=75)),
                ('contact_name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=75)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=75, serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
