from django.db import models
from client_user_panel.models import Client, ClientUser
# Create your models here.


class Cash(models.Model):
    ClientName = models.ForeignKey(Client, related_name='ownerOfThisCash')
    Balance = models.FloatField()
    DateAdded = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.ClientName