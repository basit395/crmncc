# Generated by Django 2.2.13 on 2020-12-29 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crmapp', '0007_order_mrc'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='discountmrc',
            field=models.IntegerField(default=0, verbose_name='New MRC'),
        ),
    ]
