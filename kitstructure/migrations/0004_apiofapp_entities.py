# Generated by Django 4.1.6 on 2023-09-10 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kitstructure', '0003_appobjet_comment_appobjet_db_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='apiofapp',
            name='entities',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='kitstructure.entities'),
        ),
    ]