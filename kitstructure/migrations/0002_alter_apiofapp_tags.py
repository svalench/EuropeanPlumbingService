# Generated by Django 4.1.6 on 2023-06-25 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kitstructure', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiofapp',
            name='tags',
            field=models.ManyToManyField(null=True, to='kitstructure.tagsforapi'),
        ),
    ]
