# Generated by Django 2.2.13 on 2021-04-01 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crmapp', '0033_fastdatad_datescore'),
    ]

    operations = [
        migrations.AddField(
            model_name='finvoiceitem',
            name='itemvalue',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7, verbose_name='Value'),
        ),
    ]
