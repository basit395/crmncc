# Generated by Django 2.2.13 on 2022-01-06 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_profile_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.CharField(max_length=200, null=True, verbose_name='Role'),
        ),
    ]
