# Generated by Django 2.2.13 on 2021-04-21 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crmapp', '0041_auto_20210410_0047'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='service',
            options={'ordering': ('servicename',)},
        ),
        migrations.AddField(
            model_name='fpayment',
            name='notes',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
