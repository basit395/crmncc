# Generated by Django 2.2.13 on 2021-04-01 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crmapp', '0029_auto_20210401_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finvoice',
            name='recievedamount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7, verbose_name='Recieved Amount'),
        ),
        migrations.AlterField(
            model_name='finvoice',
            name='remainingamount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7, verbose_name='Remaining Amount'),
        ),
    ]
