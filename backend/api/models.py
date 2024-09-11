from django.db import models


# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=320, unique=True)
    password = models.CharField(max_length=500)

    def __str__(self) -> str:
        return self.username
