# Generated by Django 3.0.6 on 2020-06-30 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Query",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("email", models.EmailField(max_length=254)),
                ("organisation", models.CharField(blank=True, max_length=50)),
                ("contact_number", models.CharField(max_length=13)),
                ("query", models.TextField(verbose_name="Comments")),
                ("query_date", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Staff",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("staff_name", models.CharField(max_length=50, verbose_name="Name")),
                (
                    "staff_designation",
                    models.CharField(max_length=50, verbose_name="Designation"),
                ),
                (
                    "staff_about",
                    models.CharField(
                        default="", max_length=250, verbose_name="About Staff"
                    ),
                ),
                (
                    "staff_picture",
                    models.ImageField(upload_to="staff", verbose_name="Photo "),
                ),
            ],
        ),
    ]
