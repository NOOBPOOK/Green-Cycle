from django.db import models

# Create your models here.
class Feedback(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=120)
    feedback = models.CharField(max_length=200)
    date = models.DateField()

    def __str__(self):
        return self.name

