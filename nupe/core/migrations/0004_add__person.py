# Generated by Django 3.0.6 on 2020-06-24 20:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("file", "0001_add__image_upload"),
        ("core", "0003_add__academic_education_campus__campus__institution__institution_campus"),
    ]

    operations = [
        migrations.CreateModel(
            name="Person",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("deleted", models.DateTimeField(editable=False, null=True)),
                (
                    "first_name",
                    models.CharField(
                        max_length=50,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[a-z A-Z]*$", message="Este campo deve conter somente letras"
                            )
                        ],
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        max_length=100,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[a-z A-Z]*$", message="Este campo deve conter somente letras"
                            )
                        ],
                    ),
                ),
                (
                    "cpf",
                    models.CharField(
                        max_length=11, unique=True, validators=[django.core.validators.MinLengthValidator(11)]
                    ),
                ),
                ("birthday_date", models.DateField()),
                ("gender", models.CharField(choices=[("F", "Feminino"), ("M", "Masculino")], max_length=1)),
                (
                    "contact",
                    models.CharField(
                        blank=True,
                        help_text="DDD+Número",
                        max_length=12,
                        null=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[0-9]*$", message="Este campo deve conter somente números"
                            ),
                            django.core.validators.MinLengthValidator(12),
                        ],
                    ),
                ),
                (
                    "profile_image",
                    models.OneToOneField(
                        blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="file.ProfileImage"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
            ],
            options={"abstract": False,},
        ),
    ]
