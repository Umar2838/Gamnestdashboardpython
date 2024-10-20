from django.db import models
from django.contrib.auth.models import User
import json

class Role(models.Model):
    name = models.CharField(max_length=255)  
    description = models.TextField()  
    permissions = models.JSONField(default=dict) 

    user = models.ManyToManyField(User,through='Profile')
    def __str__(self):
        return self.name

    # Method to set permissions as a JSON string
    def set_permissions(self, permissions_dict):
        self.permissions = json.dumps(permissions_dict)

    # Method to get permissions as a dictionary
    def get_permissions(self):
        return self.permissions
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    
class Venues(models.Model):
    name = models.CharField(max_length=255)
    phone = models.IntegerField()  
    email = models.EmailField(max_length=254 , unique=True)
    location = models.TextField(max_length=255)
    hours = models.TextField(max_length=255)
    locationdefine = models.TextField(max_length=255 , null=True)

    def __str__(self):
        return self.name
    
class Tickets(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    type = models.CharField(max_length=254)
    duration = models.CharField(max_length=20)
    price = models.CharField(max_length=255)

    def __str__(self):
        return self.name    
  
class Headset(models.Model):
    name = models.CharField(max_length=245)
    modelNo = models.CharField(max_length=245)
    serialNo = models.CharField(max_length=245)
    barcodeNo = models.IntegerField()
    assignedVenue = models.CharField(max_length=20)
    venue = models.ForeignKey(Venues, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
       
class Tablet(models.Model):
    name = models.CharField(max_length=245)
    modelNo = models.CharField(max_length=245)
    serialNo = models.CharField(max_length=245)
    barcodeNo = models.IntegerField()
    assignedVenue = models.CharField(max_length=20)
    venue = models.ForeignKey(Venues, on_delete=models.CASCADE)

    def __str__(self):
        return self.name       