from django.db import models

# Create your models here.


class Client(models.Model):
    ClientName = models.CharField(max_length=24, null=True, blank=True)
    Address = models.CharField(max_length=24, null=True, blank=True)
    Active = models.BooleanField(default=True)
    LastPaidAmount = models.FloatField(default=0.0)
    NumberOfUsers = models.IntegerField(default=1)
    LastDateOfPayment = models.DateTimeField(auto_now=False, auto_now_add=True)
    DateAdded = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.ClientName


class ClientUser(models.Model):
    Client = models.ForeignKey(Client, related_name='NameOfTheClient')
    username = models.CharField(max_length=24, null=True, blank=True)
    Name = models.CharField(max_length=24, null=True, blank=True)
    Email = models.EmailField()
    Phone = models.CharField(max_length=15, null=True, blank=True)
    Admin = models.BooleanField(default=False)
    Active = models.BooleanField(default=True)
    DateAdded = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.username


class ClientUserSuggestionNames(models.Model):
    Client = models.ForeignKey(Client, related_name='ClientNameSuggestion')
    ClientNameSuggestion = models.CharField(max_length=24, null=True, blank=True)
    DateAdded = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.Client


class ClientUserSuggestionPurpose(models.Model):
    Client = models.ForeignKey(Client, related_name='ClientPurposeSuggestion')
    ClientPurposeSuggestion = models.CharField(max_length=24, null=True, blank=True)
    DateAdded = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.Client