# Generated by Django 2.2.5 on 2019-10-30 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsTonalDaily',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tonality', models.CharField(choices=[(0, 'Neutral'), (1, 'Positive'), (-1, 'Negative')], default=0, max_length=10, verbose_name='Tonality')),
                ('tonality_index', models.IntegerField(default=0, verbose_name='Tonality index')),
                ('date', models.DateTimeField(verbose_name='Date')),
            ],
            options={
                'verbose_name': 'Daily tonality',
                'verbose_name_plural': 'Daily tonalities',
            },
        ),
    ]
