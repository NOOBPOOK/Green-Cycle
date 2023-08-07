from django.db import models
import datetime


class Feedback(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=120)
    feedback = models.CharField(max_length=200)
    date = models.DateField()

    def __str__(self):
        return self.email

class MetalRequest(models.Model):
    fname = models.CharField(max_length=120)
    lname = models.CharField(max_length=120)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=10)
    kg = models.CharField(max_length=5)
    category = models.CharField(max_length=20)
    description = models.CharField(max_length=500)
    date = models.DateField()

    def __str__(self):
        return self.email
    
class PaperRequest(models.Model):
    fname = models.CharField(max_length=120)
    lname = models.CharField(max_length=120)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=10)
    kg = models.CharField(max_length=5)
    category = models.CharField(max_length=20)
    description = models.CharField(max_length=500)
    date = models.DateField()

    def __str__(self):
        return self.email
    
class GlassRequest(models.Model):
    fname = models.CharField(max_length=120)
    lname = models.CharField(max_length=120)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=10)
    kg = models.CharField(max_length=5)
    category = models.CharField(max_length=20)
    description = models.CharField(max_length=500)
    date = models.DateField()

    def __str__(self):
        return self.email
    
class PlasticRequest(models.Model):
    fname = models.CharField(max_length=120)
    lname = models.CharField(max_length=120)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=10)
    kg = models.CharField(max_length=5)
    category = models.CharField(max_length=20)
    description = models.CharField(max_length=500)
    date = models.DateField()

    def __str__(self):
        return self.email
    
class ClothesRequest(models.Model):
    fname = models.CharField(max_length=120)
    lname = models.CharField(max_length=120)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=10)
    kg = models.CharField(max_length=5)
    category = models.CharField(max_length=20)
    description = models.CharField(max_length=500)
    date = models.DateField()

    def __str__(self):
        return self.email
    
class EwasteRequest(models.Model):
    fname = models.CharField(max_length=120)
    lname = models.CharField(max_length=120)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=10)
    kg = models.CharField(max_length=5)
    category = models.CharField(max_length=20)
    description = models.CharField(max_length=500)
    date = models.DateField()

    def __str__(self):
        return self.email