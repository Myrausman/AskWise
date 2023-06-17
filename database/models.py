from django.db import models

# Create your models here.
class Login(models.Model):
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=25)

class Question(models.Model):
    title = models.TextField()
    detail = models.TextField()
    tags = models.TextField()
