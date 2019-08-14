# Generated by Django 2.1.5 on 2019-08-14 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0002_homepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_carousel', models.ImageField(height_field=100, upload_to='carousel', width_field=500)),
                ('title', models.CharField(max_length=20)),
                ('detail', models.CharField(max_length=80)),
            ],
        ),
    ]
