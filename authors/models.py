from django.db import models
from datetime import datetime
# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
