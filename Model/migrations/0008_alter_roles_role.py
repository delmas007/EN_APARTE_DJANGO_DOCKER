# Generated by Django 4.2.7 on 2023-12-06 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Model', '0007_commande_produit_alter_roles_role_lignecommande_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roles',
            name='role',
            field=models.CharField(choices=[('ADMIN', 'ADMIN'), ('EMPLOYER', 'EMPLOYER'), ('VENDEUR', 'VENDEUR'), ('CLIENT', 'CLIENT')], max_length=10),
        ),
    ]
