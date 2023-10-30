from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Account(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    addres=models.CharField(default="")
    mobile=models.CharField(max_length=13, default="")
    city=models.CharField(default="")
    psc=models.CharField(default="")
    CZK = models.FloatField(default=(0.0))
    kid1= models.CharField(default="")
    kid2= models.CharField(default="")
    kid3= models.CharField(default="")
    kid4= models.CharField(default="")
    position=models.IntegerField(default=0)
    events = models.ManyToManyField('Event', related_name='accounts', blank=True)
    objects = models.Manager()

class Event(models.Model):
    creater=models,models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=80)
    destination=models.CharField(max_length=50)
    meeting=models.DateTimeField()
    ending=models.DateTimeField()
    departure=models.CharField(max_length=100)
    arrival=models.CharField(max_length=100)
    notes=models,models.CharField(default="Dobrou náladu")
    people=models.ManyToManyField(Account, related_name='accounts', blank=True)
    objects = models.Manager()
    
    