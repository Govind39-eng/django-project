from django.db import models

# Create your models here.
class Account(models.Model):
    acno = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    address = models.TextField()
    contactno = models.CharField(max_length=15)
    emailaddress = models.CharField(max_length=50)
    panno = models.CharField(max_length=10)
    aadharno = models.CharField(max_length=12)
    balance = models.IntegerField()
    password = models.CharField(max_length=20)

class AdminLogin(models.Model):
    userid = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=20)
class Statement(models.Model):
    fromaccount = models.IntegerField()
    toaccount = models.IntegerField()
    operation = models.CharField(max_length=20)
    amount = models.IntegerField()
    opdate = models.CharField(max_length=30)