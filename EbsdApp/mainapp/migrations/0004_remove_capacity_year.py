# Generated by Django 2.2.9 on 2020-02-16 17:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_csvpath'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='capacity',
            name='year',
        ),
    ]
