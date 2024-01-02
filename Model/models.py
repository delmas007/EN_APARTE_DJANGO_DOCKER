import uuid
from datetime import timedelta
from decimal import Decimal
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.dispatch import receiver

from APPARTE import settings

# Create your models here.
sex = (
    ('Homme', 'Homme'),
    ("Femme", "Femme"),
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Vous devez entrer un mail")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_admin = True
        user.save()
        return user


class Roles(models.Model):
    ADMIN = 'ADMIN'
    EMPLOYER = 'EMPLOYER'
    VENDEUR = 'VENDEUR'
    CLIENT = 'CLIENT'

    ROLE_CHOICES = [
        (ADMIN, 'ADMIN'),
        (EMPLOYER, 'EMPLOYER'),
        (VENDEUR, 'VENDEUR'),
        (CLIENT, 'CLIENT'),

    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.get_role_display()


class Utilisateur(AbstractBaseUser):
    mon_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    email = models.EmailField(
        unique=True,
        max_length=255,
        blank=False
    )
    nom = models.CharField(max_length=250, verbose_name='nom')
    prenom = models.CharField(max_length=250)
    contact = models.IntegerField()
    commune = models.CharField(max_length=250)
    sexe = models.CharField(blank=False, choices=sex, max_length=6)
    roles = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name = 'utilisateur'

    def __str__(self):
        return self.nom


class Service(models.Model):
    type = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    disponibilite = models.BooleanField(default=True)

    def __str__(self):
        if self.disponibilite:
            return self.type


class horaire(models.Model):
    heure = models.CharField(max_length=255, blank=False)
    disponibilite = models.BooleanField(default=True)

    def __str__(self):
        if self.disponibilite:
            return self.heure
        else:
            return ""


class Rendez_vous(models.Model):
    date_rendez_vous = models.DateField(blank=True, null=True)
    en_attente = models.BooleanField(default=True)
    confirmation = models.BooleanField(default=False)
    debut = models.BooleanField(default=False)
    fin = models.BooleanField(default=False)
    Date_prise_rendez_vous = models.DateTimeField(null=True, blank=True)
    heure_debut_rendez_vous = models.TimeField(null=True, blank=True)
    heure_fin_rendez_vous = models.TimeField(null=True, blank=True)
    duree_rendez_vous = models.DurationField(null=True, blank=True)
    client = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, related_name='rendez_vous_clients')
    employer = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True,
                                 related_name='rendez_vous_employers')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True,related_name='services')
    horaire = models.ForeignKey(horaire, on_delete=models.SET_NULL, null=True)
    etat = models.CharField(max_length=255,null=True,blank=True)
    preference_employer = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True,
                                            related_name='rendez_vous_preference_employer')

    def save(self, *args, **kwargs):
        # Calculez l'état lors de la sauvegarde du modèle
        if self.en_attente:
            self.etat = "Reservation pas encore accepter"
        elif self.debut and not self.fin:
            self.etat = "en cours..."
        elif self.fin:
            self.etat = "Terminé"
        elif not self.debut:
            self.etat = "Pas encore commencé"

        super().save(*args, **kwargs)



@receiver(pre_save, sender=Rendez_vous)
def update_dates_heures_rendez_vous(sender, instance, **kwargs):
    if instance.debut and not instance.heure_debut_rendez_vous:
        instance.heure_debut_rendez_vous = timezone.now().time()

    if instance.fin and not instance.heure_fin_rendez_vous:
        instance.heure_fin_rendez_vous = timezone.now().time()

    if instance.confirmation and not instance.Date_prise_rendez_vous:
        instance.Date_prise_rendez_vous = timezone.now()

    if instance.heure_debut_rendez_vous and instance.heure_fin_rendez_vous:
        duree = timezone.datetime.combine(timezone.now().date(),
                                          instance.heure_fin_rendez_vous) - timezone.datetime.combine(
            timezone.now().date(), instance.heure_debut_rendez_vous)

        # Convertir la différence en timedelta
        duree_timedelta = timedelta(seconds=duree.total_seconds())

        # Affecter la valeur à duree_rendez_vous
        instance.duree_rendez_vous = duree_timedelta


class Produit(models.Model):
    employer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                 related_name='produits_ajoutes')
    nom = models.CharField(max_length=255)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    prix_reduit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    promotion = models.BooleanField(default=False)
    pourcentage_promotion = models.IntegerField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='image_produit/')

    def get_prix_reduit(self):
        if self.promotion and self.pourcentage_promotion:
            return Decimal(str(self.prix_reduit))  # Convertit en Decimal
        else:
            return Decimal(str(self.prix))

    def save(self, *args, **kwargs):
        action = 'modification' if self.pk else 'ajout'
        if self.promotion and self.pourcentage_promotion:
            self.prix_reduit = self.prix - (self.prix * self.pourcentage_promotion / 100)
        else:
            self.prix_reduit = None  # Remettre à None si pas de promotion

        super().save(*args, **kwargs)
        ProduitLog.objects.create(
            produit=self,
            action=action,
            utilisateur=self.employer,
            nom_produit=self.nom,
            prix_produit=self.prix,
        )

    def delete(self, *args, **kwargs):
        # Sauvegarde des informations avant la suppression du produit
        produit_log = ProduitLog.objects.create(
            produit=self,
            action='suppression',
            utilisateur=self.employer,
            nom_produit=self.nom,
            prix_produit=self.prix,
        )

        super().delete(*args, **kwargs)


class ProduitLog(models.Model):
    ACTION_CHOICES = [
        ('ajout', 'Ajout'),
        ('modification', 'Modification'),
        ('suppression', 'Suppression'),
    ]

    produit = models.ForeignKey('Produit', on_delete=models.SET_NULL, null=True, related_name='produit_logs')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True)
    nom_produit = models.CharField(max_length=255, null=True)
    prix_produit = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    # Ajoutez d'autres champs pour enregistrer les détails de l'action si nécessaire

    # def save(self, *args, **kwargs):
    #     # Sauvegarde des informations avant l'action
    #     if self.action in ['ajout', 'modification']:
    #         self.nom_produit = self.produit.nom
    #         self.prix_produit = self.produit.prix
    #
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.get_action_display()} sur {self.nom_produit} par {self.utilisateur.nom}'


class Commande(models.Model):
    client = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True,
                               related_name='commande_client')
    produits = models.ForeignKey(Produit, on_delete=models.SET_NULL, null=True, )
    quantite = models.IntegerField(default=1)

    def __str__(self):
        return f"Commande #{self.pk} - {self.client.nom} "

    @property
    def total_commande(self):
        return self.produits.get_prix_reduit() * self.quantite


class Paniers(models.Model):
    client = models.ForeignKey('Utilisateur', on_delete=models.SET_NULL, null=True)
    employer = models.ForeignKey('Utilisateur', on_delete=models.SET_NULL, null=True, related_name='commande_employers')
    ordre = models.ManyToManyField(Commande)
    date_commande_client = models.DateTimeField(null=True, blank=True)
    date_confirmation_commande = models.DateTimeField(null=True, blank=True)
    date_reception_commande = models.DateTimeField(null=True, blank=True)
    montant_total = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    confirmation_panier = models.BooleanField(default=False)
    confirmation_employer = models.BooleanField(default=False)
    reception_commande = models.BooleanField(default=False)
    statut = models.CharField(
        max_length=50,
        choices=[
            ('En attente', 'En attente'),
            ('En cours de traitement', 'En cours de traitement'),
            ('Expédiée', 'Expédiée')
        ],
        default='En attente'
    )

    def calculer_montant_total(self):
        total = sum(commande.total_commande for commande in self.ordre.all())
        return total

    def save(self, *args, **kwargs):
        if self.confirmation_panier and not self.date_commande_client:
            self.date_commande_client = timezone.now()

        if self.confirmation_employer and not self.date_confirmation_commande:
            self.date_confirmation_commande = timezone.now()

        if self.reception_commande and not self.date_reception_commande:
            self.date_reception_commande = timezone.now()

        super().save(*args, **kwargs)

    def supprimer_panier(self):
        self.ordre.all().delete()
        self.delete()
