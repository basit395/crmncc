# Generated by Django 2.2.13 on 2021-08-25 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crmapp', '0051_orderimport'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounts',
            name='ispayed',
            field=models.BooleanField(default=False, verbose_name='Is payed'),
        ),
    ]
