# Generated by Django 2.2.3 on 2019-09-11 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('kind', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('description', models.TextField(max_length=250)),
            ],
        ),
    ]
