# Generated by Django 4.2.7 on 2024-01-03 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Model', '0008_rendez_vous_commentaire_rendez_vous_mot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rendez_vous',
            name='mot',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
