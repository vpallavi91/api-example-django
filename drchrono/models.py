from django.db import models

# Create your models here.

class PatientModel(models.Model):
    fname = models.CharField(max_length=50,null=False)
    lname = models.CharField(max_length=50,null=True)
    email = models.CharField(max_length=50,null=True)
    dob   = models.CharField(max_length=10,null=True)
    gender= models.CharField(max_length=6,null=True)
    mailsent = models.BooleanField(default=False)

    def __str__(self):
        return self.fname + ' ' + self.lname

    class Meta:
        ordering = ['dob']
