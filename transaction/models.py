from django.db import models
from client_user_panel.models import Client, ClientUser
from bank.models import Bank

# Create your models here.


class Transaction(models.Model):
    Client = models.ForeignKey(Client, related_name='NameOfTheClientWhoDidThisTransaction')
    Purpose = models.CharField(max_length=24, null=True, blank=True)
    TransactionWith = models.CharField(max_length=24, null=True, blank=True)
    Amount = models.FloatField()
    EntryBy = models.ForeignKey(ClientUser, related_name='whoEnteredTheValues')
    Type = models.CharField(max_length=124, null=True, blank=True)
    Bank = models.ForeignKey(Bank, related_name='theBankID', null=True, blank=True)
    Remarks = models.CharField(max_length=124, null=True, blank=True)
    Received = models.BooleanField(default=True)
    DateAdded = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.Client


class BorrowedTransaction(models.Model):
    transaction = models.ForeignKey(Transaction, related_name='theTransactionWith')
    NextDate = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    Paid = models.BooleanField(default=False)
    DateAdded = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return self.transaction


class LentTransaction(models.Model):
    transaction = models.ForeignKey(Transaction, related_name='theTransactionWithLent')
    NextDate = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    Paid = models.BooleanField(default=False)
    DateAdded = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return self.transaction