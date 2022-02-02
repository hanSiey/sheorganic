from django.db import models
# Create your models here.

class Distributor(models.Model):
     STATUS = (
        ('Active', 'Active'),
        ('Not Available', 'Not Available'),
     )
     name = models.CharField(max_length=20)
     surname = models.CharField(max_length=20, null=True)
     phone = models.CharField(max_length=15, null=True)
     email = models.EmailField()
     area_of_operation = models.CharField(max_length=200)
     status = models.CharField(max_length=20, null=True, blank=True, choices=STATUS, default="Active") 
     def __str__(self):
         return self.name
