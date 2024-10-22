# Generated by Django 5.0.7 on 2024-07-25 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0001_add__account"),
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="deleted_by_cascade",
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name="account",
            name="deleted",
            field=models.DateTimeField(db_index=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name="account",
            name="id",
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
        ),
    ]