# Generated by Django 4.2.3 on 2023-07-24 21:23

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import utils.validators


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Person",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("address", models.CharField(max_length=100)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Rut",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "code",
                    models.CharField(
                        db_index=True,
                        max_length=10,
                        unique=True,
                        validators=[utils.validators.rut_validator],
                    ),
                ),
                ("name", models.CharField(max_length=200)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Society",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("actions", models.PositiveIntegerField(default=0)),
            ],
            options={
                "verbose_name_plural": "societies",
            },
        ),
        migrations.CreateModel(
            name="SocietyMember",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("actions", models.PositiveIntegerField(default=0)),
                (
                    "member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="societies.person",
                    ),
                ),
                (
                    "society",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="societies.society",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="SocietyAdmin",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "faculties",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=50), size=None
                    ),
                ),
                (
                    "admin",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="societies.person",
                    ),
                ),
                (
                    "society",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="societies.society",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="society",
            name="admins",
            field=models.ManyToManyField(
                related_name="admin_society",
                through="societies.SocietyAdmin",
                to="societies.person",
            ),
        ),
        migrations.AddField(
            model_name="society",
            name="members",
            field=models.ManyToManyField(
                related_name="member_society",
                through="societies.SocietyMember",
                to="societies.person",
            ),
        ),
        migrations.AddField(
            model_name="society",
            name="rut",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="societies.rut"
            ),
        ),
        migrations.AddField(
            model_name="person",
            name="rut",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="societies.rut"
            ),
        ),
    ]
