# Generated by Django 2.2.13 on 2021-08-12 07:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crmapp', '0049_auto_20210811_1656'),
    ]

    operations = [
        migrations.CreateModel(
            name='company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyname', models.CharField(max_length=100, unique=True, verbose_name='Company')),
                ('creationdate', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
            ],
            options={
                'verbose_name_plural': 'Companies',
                'verbose_name': 'Company',
            },
        ),
        migrations.CreateModel(
            name='project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projectname', models.CharField(max_length=100, verbose_name='Company')),
                ('creationdate', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_projects', to='crmapp.company', verbose_name='Project')),
            ],
            options={
                'verbose_name_plural': 'Projects',
                'unique_together': {('projectname', 'company')},
                'verbose_name': 'Project',
            },
        ),
    ]
