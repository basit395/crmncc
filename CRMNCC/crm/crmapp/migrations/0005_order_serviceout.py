# Generated by Django 2.2.13 on 2020-12-29 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crmapp', '0004_order_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='serviceout',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='service out'),
        ),
    ]
