# Generated by Django 4.1.13 on 2023-12-19 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Model', '0020_remove_commande_confirmer_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='horaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heure', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='rendez_vous',
            name='horaire',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Model.horaire'),
        ),
    ]
