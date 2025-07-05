from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLES = [
        ("utilisateur", "Utilisateur"),
        ("agent", "Agent"),
        ("admin", "Admin"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLES, default="utilisateur", blank=True)
    photo = models.ImageField(upload_to="profiles/", null=True, blank=False)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Signalement(models.Model):
    CATEGORIES = [
        ('lampadaire', 'Lampadaire'),
        ('nid_de_poule', 'Nid-de-poule'),
        ('fuite', 'Fuite d’eau'),
        ('autre', 'Autre'),
        ('erosion', 'Érosion'),
        ('incendie', 'Incendie'),
    ]
    STATUTS = [
        ('nouveau', 'Nouveau'),
        ('pris', 'Pris en charge'),
        ('en_cours', 'En cours'),
        ('resolu', 'Résolu'),
        ('rejete', 'Rejeté'),
    ]

    profil = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    titre = models.CharField(max_length=100)
    description = models.TextField()
    categorie = models.CharField(max_length=20, choices=CATEGORIES , default='autre')
    statut = models.CharField(max_length=20, choices=STATUTS, default='nouveau')
    latitude = models.FloatField()
    longitude = models.FloatField()
    photo = models.ImageField(upload_to='signalements/', blank=True, null=True)
    date_signalement = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre
