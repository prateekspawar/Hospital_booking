from django.shortcuts import render
from django.db import models
import datetime
import time
from django.utils import timezone


class Doc(models.Model):
    user_name = models.CharField(max_length=200)
    user_pass = models.CharField(max_length=200)
    user_first= models.CharField(max_length=200)
    user_last=  models.CharField(max_length=200)
    user_email= models.EmailField(max_length=300)
    def __str__(self):
        return self.user_name
    


class Hos(models.Model):
    hos_name = models.CharField(max_length=200)
    hos_pass = models.CharField(max_length=200)
    hos_email= models.EmailField(max_length=300)
    def __str__(self):
        return self.hos_name





class Bed(models.Model):
    hospital =   models.ForeignKey(Hos, on_delete=models.CASCADE)
    bed_type =   models.IntegerField()
    occu =       models.BooleanField()
    
class Booking(models.Model):
    bed =   models.ForeignKey(Bed,on_delete=models.CASCADE)
    bed_type= models.IntegerField(default=1)
    doctor =   models.ForeignKey(Doc,on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=200,default='patient_name')
    patient_mob = models.CharField(max_length=10,default='78946')
    date=   models.DateTimeField()
    
    
    