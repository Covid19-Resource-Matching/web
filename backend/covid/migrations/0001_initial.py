# Generated by Django 3.0.4 on 2020-03-17 00:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Descriptor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('permanent', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Fulfillment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('assigned', models.DateTimeField(null=True)),
                ('collected', models.DateTimeField(null=True)),
                ('completed', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Supply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('descriptor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='covid.Descriptor')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='covid.Supplier')),
            ],
        ),
        migrations.CreateModel(
            name='Requester',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('descriptor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='covid.Descriptor')),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='covid.Requester')),
            ],
        ),
    ]
