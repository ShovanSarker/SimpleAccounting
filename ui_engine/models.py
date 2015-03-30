from django.db import models

# Create your models here.


class PasswordRecover(models.Model):
    Username = models.CharField(max_length=32, null=True, blank=True)
    Code = models.CharField(max_length=32, null=True, blank=True)
    Hit = models.BooleanField(default=False)
    DateAdded = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.Username