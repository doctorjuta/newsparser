# Generated by Django 2.2.5 on 2019-11-08 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0010_auto_20191107_1549'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Name')),
                ('text', models.TextField(verbose_name='Text')),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
            },
        ),
    ]
