# Generated by Django 5.0.1 on 2024-05-20 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Todotable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taskname', models.TextField(blank=True, null=True)),
                ('date', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'todotable',
                'managed': False,
            },
        ),
    ]
