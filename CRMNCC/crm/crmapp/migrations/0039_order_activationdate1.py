# Generated by Django 2.2.13 on 2021-04-09 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crmapp', '0038_order_commission'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='activationdate1',
            field=models.DateField(blank=True, null=True, verbose_name='Activation Date'),
        ),
    ]
