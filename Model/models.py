from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.dispatch import receiver

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
    EMPLOYER = 'EMPLOYER'
    CLIENT = 'CLIENT'
    ADMIN = 'ADMIN'

    ROLE_CHOICES = [
        (EMPLOYER, 'EMPLOYER'),
        (CLIENT, 'CLIENT'),
        (ADMIN, 'CLIENT'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.get_role_display()


class Utilisateur(AbstractBaseUser):
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


class Rendez_vous(models.Model):
    TYPE_MASSAGE_CHOICES = [
        ('massage', 'Massage'),
        ('coiffure', 'Coiffure'),
        ('soins_peau', 'Soins de peau'),
    ]
    TIME = [
        ('8H00-10H00', '8H00-10H00'),
        ('10H00-12H00', '10H00-12H00'),
        ('14H00-16H00', '14H00-16H00'),
        ('16H00-18H00', '16H00-18H00'),
    ]
    date_rendez_vous = models.DateField(blank=True,null=True)
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
    heure_rendez_vous = models.CharField(blank=True,null=True,choices=TIME)

    type_massage = models.CharField(max_length=255, choices=TYPE_MASSAGE_CHOICES, null=True)


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
        instance.duree_rendez_vous = duree.total_seconds() // 60
