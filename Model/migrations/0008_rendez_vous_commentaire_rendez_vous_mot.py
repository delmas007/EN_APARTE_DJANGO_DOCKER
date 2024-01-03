
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Model', '0007_rendez_vous_eva_uuid_rendez_vous_evaluation'),
    ]

    operations = [
        migrations.AddField(
            model_name='rendez_vous',
            name='commentaire',
            field=models.TextField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='rendez_vous',
            name='mot',
            field=models.CharField(blank=True, choices=[('Homme', 'Homme'), ('Femme', 'Femme')], max_length=250, null=True),
        ),
    ]
