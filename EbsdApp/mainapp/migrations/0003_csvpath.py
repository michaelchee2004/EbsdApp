# Generated by Django 2.2.9 on 2020-02-16 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20200215_2331'),
    ]

    operations = [
        migrations.CreateModel(
            name='CsvPath',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=200)),
            ],
        ),
    ]
