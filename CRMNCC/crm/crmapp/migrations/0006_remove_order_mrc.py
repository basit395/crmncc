# Generated by Django 2.2.13 on 2020-12-29 21:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crmapp', '0005_order_serviceout'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='mrc',
        ),
    ]
