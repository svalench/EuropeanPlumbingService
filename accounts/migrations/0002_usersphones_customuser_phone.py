# Generated by Django 4.1.6 on 2023-02-09 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UsersPhones",
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
                (
                    "phone",
                    models.CharField(max_length=40, unique=True, verbose_name="phone"),
                ),
            ],
        ),
        migrations.AddField(
            model_name="customuser",
            name="phone",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="accounts.usersphones",
                verbose_name="User phones",
            ),
        ),
    ]
