# Generated by Django 2.1.5 on 2019-08-14 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0003_carousel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carousel',
            name='image_carousel',
            field=models.ImageField(upload_to='carousel'),
        ),
    ]
