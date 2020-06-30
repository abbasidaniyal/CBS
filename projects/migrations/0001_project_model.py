# Generated by Django 3.0.6 on 2020-06-30 14:38

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=100, verbose_name="Client's Name")),
                ('client_logo', models.ImageField(upload_to='client_logos', verbose_name="Client's Logo")),
                ('client_website', models.URLField(blank=True, verbose_name="Client's Website")),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=100, verbose_name='Project Name')),
                ('city', models.CharField(max_length=200, verbose_name='Site Location')),
                ('project_description', models.TextField(max_length=300, verbose_name='Project Description')),
                ('architect', models.CharField(blank=True, max_length=50, verbose_name='Architect')),
                ('expertise', multiselectfield.db.fields.MultiSelectField(choices=[('SS', 'Steel Structures'), ('TMS', 'Tensile Membrane Structures'), ('RF', 'Roofings'), ('CD', 'Claddings'), ('SS', 'Services'), ('SC', 'Studio Connect')], default=[('SS', 'Steel Structures'), ('TMS', 'Tensile Membrane Structures'), ('RF', 'Roofings'), ('CD', 'Claddings'), ('SS', 'Services'), ('SC', 'Studio Connect')], max_length=18)),
                ('year', models.IntegerField(verbose_name='Year Completed')),
                ('client', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='projects.Client')),
            ],
        ),
        migrations.CreateModel(
            name='GalleryImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='gallery', verbose_name='Image')),
                ('image_description', models.CharField(blank=True, max_length=50, verbose_name='Image Description')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='projects.Project', verbose_name='Project')),
            ],
        ),
    ]
