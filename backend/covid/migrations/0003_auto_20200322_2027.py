# Generated by Django 3.0.4 on 2020-03-23 00:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0002_auto_20200316_2056'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='timestamp',
        ),
        migrations.RemoveField(
            model_name='supply',
            name='timestamp',
        ),
    ]