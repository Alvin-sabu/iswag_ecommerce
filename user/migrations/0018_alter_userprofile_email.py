# Generated by Django 5.0.1 on 2024-04-15 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
