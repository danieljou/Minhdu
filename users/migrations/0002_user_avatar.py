# Generated by Django 4.0.1 on 2022-09-22 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='Avatar',
            field=models.ImageField(null=True, upload_to='avatars'),
        ),
    ]
