from django.db import models

class CustomUser(models.Model):
  email = models.CharField(unique=True,max_length=255)
  name = models.CharField(max_length=255)
  picture = models.CharField(max_length=255)

  def __str__(self):
    return self.email
# Create your models here.
