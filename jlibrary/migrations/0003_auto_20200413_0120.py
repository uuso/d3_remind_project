# Generated by Django 2.2.12 on 2020-04-12 22:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jlibrary', '0002_auto_20200406_2319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booklease',
            name='leaseover_date',
            field=models.DateField(default=datetime.datetime(2020, 4, 27, 1, 20, 29, 42376)),
        ),
    ]
