# Generated by Django 2.2.5 on 2019-10-30 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0004_auto_20191030_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newstonaldaily',
            name='tonality_index',
            field=models.FloatField(default=0.0, verbose_name='Tonality index'),
        ),
    ]
