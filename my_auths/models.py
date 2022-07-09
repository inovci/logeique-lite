from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Landlord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='landlord')
    contact = models.CharField(max_length=50)
    avatar = models.ImageField(null=True, blank=True, upload_to="img/avatars/", default="img/avatars/default-user-img.png")

    class Meta():
        ordering = ['user', 'contact']

    def __str__(self):
        return f"Statut: Propriétaire - User: {self.user} - Contact: {self.contact}"

    def statuLogeique(self):
        return f"Propriétaire"


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client')
    contact = models.CharField(max_length=50)
    avatar = models.ImageField(null=True, blank=True, upload_to="img/avatars/", default="img/avatars/default-user-img.png")

    class Meta():
        ordering = ['user', 'contact']

    def __str__(self):
        return f"Statut: Client - User: {self.user} - Contact: {self.contact}"

    def statuLogeique(self):
        return f"Client"


class Maison(models.Model):
    ville = models.CharField(max_length=100)
    quartier = models.CharField(max_length=100)
    loyer = models.BigIntegerField(null=True)
    cotion = models.BigIntegerField(null=True)
    type_maison = models.CharField(max_length=200)
    nombre_piece = models.IntegerField(null=True)
    en_location = models.BooleanField(default=False, null=True, blank=True)
    en_vente = models.BooleanField(default=False, null=True, blank=True)
    photos = models.ImageField(null=True, blank=True, upload_to="img/maisons/")
    quan_dispo = models.IntegerField(null=True, blank=True, default=1)
    ajoute_le = models.DateField(auto_now_add=True)
    edite_le = models.DateField(auto_now=True)
    occupee = models.BooleanField(default=False)
    occupant = models.CharField(max_length=200, null=True, blank=True)
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE, related_name="maisons")

    def __str__(self):
        return f"Ville: {self.ville} - Quartier: {self.quartier} - Loyer: {self.loyer}"


class Proposal(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="proposals")
    loyer_du_client = models.BigIntegerField(null=True)
    cotion_du_client = models.BigIntegerField(null=True)
    type_du_client = models.CharField(max_length=50, null=True, default=None)
    nombre_piece_desire = models.IntegerField(null=True, default=None)
    zone_desire = models.CharField(max_length=50, null=True, default=None)
    ville_desire = models.CharField(max_length=50, null=True, default=None)

    class Meta():
        ordering = ['client', 'loyer_du_client', 'cotion_du_client']

    def __str__(self):
        return f"{self.id} - {self.client}"