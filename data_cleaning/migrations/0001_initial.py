# Generated by Django 2.2 on 2019-10-18 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iswc', models.CharField(max_length=50)),
                ('tittle', models.CharField(max_length=50)),
                ('contributors', models.ManyToManyField(to='data_cleaning.Contributor')),
            ],
        ),
    ]
