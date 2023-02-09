# Generated by Django 4.1.6 on 2023-02-09 16:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_usersphones_customuser_phone"),
    ]

    operations = [
        migrations.RemoveField(model_name="customuser", name="phone",),
        migrations.AddField(
            model_name="usersphones",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="User",
            ),
        ),
    ]
