# Generated by Django 2.2.1 on 2019-08-16 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0020_auto_20190816_0114'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='staff_about',
            field=models.CharField(default='', max_length=250, verbose_name='About Staff'),
        ),
    ]