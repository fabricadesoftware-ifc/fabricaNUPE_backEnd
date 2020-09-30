# Generated by Django 3.1 on 2020-09-30 23:36

import django.db.models.deletion
from django.db import migrations, models

import nupe.account.models.account


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("core", "0006_add__function__sector"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Account",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("deleted", models.DateTimeField(editable=False, null=True)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("date_joined", models.DateField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=True)),
                (
                    "function",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="workers",
                        related_query_name="worker",
                        to="core.function",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "local_job",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="workers",
                        related_query_name="worker",
                        to="core.institutioncampus",
                    ),
                ),
                (
                    "person",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="account",
                        to="core.person",
                    ),
                ),
                (
                    "sector",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="workers",
                        related_query_name="worker",
                        to="core.sector",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={"abstract": False,},
            managers=[("objects", nupe.account.models.account.AccountManager()),],
        ),
    ]
