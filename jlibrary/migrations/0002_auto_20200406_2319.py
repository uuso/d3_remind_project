# Generated by Django 2.2.11 on 2020-04-06 20:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jlibrary', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='photo',
            field=models.ImageField(blank=True, upload_to='jlibrary/images/author/'),
        ),
        migrations.AddField(
            model_name='book',
            name='photo',
            field=models.ImageField(blank=True, upload_to='jlibrary/images/book/'),
        ),
        migrations.AlterField(
            model_name='booklease',
            name='leaseover_date',
            field=models.DateField(default=datetime.datetime(2020, 4, 20, 23, 19, 2, 602953)),
        ),
    ]
