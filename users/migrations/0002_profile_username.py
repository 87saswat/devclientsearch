# Generated by Django 3.1.11 on 2022-07-27 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='username',
            field=models.EmailField(blank=True, max_length=200, null=True),
        ),
    ]
