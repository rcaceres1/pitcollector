from django.db import models
from django.urls import reverse

# Create your models here.
class Pit(models.Model): 
    name = models.CharField(max_length=100)
    kind = models.CharField(max_length=100)
    age = models.IntegerField()
    description = models.TextField(max_length=250)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pit_id': self.id})
        