# Generated by Django 4.0.1 on 2022-08-17 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Avis', models.BooleanField()),
                ('commentaire', models.TextField(blank=True, null=True)),
                ('Justificatif', models.ImageField(blank=True, null=True, upload_to='demandeok')),
                ('demande', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='demande', to='main.demandeur')),
            ],
        ),
    ]
