# Generated by Django 2.1.5 on 2019-08-15 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=50, verbose_name="Client's Name")),
                ('client_logo', models.ImageField(upload_to='clients', verbose_name="Client's Logo")),
            ],
        ),
        migrations.CreateModel(
            name='GalleryImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='gallery', verbose_name='Image')),
            ],
        ),
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=50, verbose_name='Project Name')),
                ('project_location', models.CharField(max_length=50, verbose_name='Site Address')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Clients')),
            ],
        ),
        migrations.AddField(
            model_name='galleryimage',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Projects'),
        ),
    ]
