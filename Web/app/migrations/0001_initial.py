# Generated by Django 4.1 on 2024-12-15 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Laptop",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("brand", models.CharField(max_length=50)),
                ("price", models.DecimalField(decimal_places=2, max_digits=15)),
                ("old", models.IntegerField()),
                ("new", models.IntegerField()),
                ("cpu", models.CharField(max_length=100)),
                ("cpu_brand", models.CharField(max_length=50)),
                ("ram_capacity", models.CharField(max_length=50)),
                ("ram_brand", models.CharField(max_length=50)),
                ("hard_drive_type", models.CharField(max_length=50)),
                ("hard_drive_capacity", models.CharField(max_length=50)),
                ("card", models.CharField(max_length=100)),
                ("card_brand", models.CharField(max_length=50)),
                ("screen_size", models.CharField(max_length=50)),
                ("screen_type", models.CharField(max_length=50)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "laptops",
            },
        ),
    ]
