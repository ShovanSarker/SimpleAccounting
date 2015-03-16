from django.db import models
from client_user_panel.models import Client, ClientUser
# Create your models here.


class Bank(models.Model):
    ClientName = models.ForeignKey(Client, related_name='ownerOfThisAccount')
    NameOfTheBank = models.CharField(max_length=124, null=True, blank=True)
    AccountNumber = models.CharField(max_length=124, null=True, blank=True)
    Balance = models.FloatField()
    Active = models.BooleanField(default=True)
    DateAdded = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.ClientName