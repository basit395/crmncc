# Generated by Django 2.2.13 on 2021-06-09 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crmapp', '0046_auto_20210609_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounts',
            name='activationdate',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Activation Date'),
        ),
    ]
