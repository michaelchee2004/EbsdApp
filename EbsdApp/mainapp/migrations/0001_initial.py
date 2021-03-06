# Generated by Django 2.2.9 on 2020-02-15 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year_value', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Opex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Option')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Year')),
            ],
        ),
        migrations.CreateModel(
            name='Demand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Year')),
            ],
        ),
        migrations.CreateModel(
            name='Capital',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Option')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Year')),
            ],
        ),
        migrations.CreateModel(
            name='Capacity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Option')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Year')),
            ],
        ),
    ]
