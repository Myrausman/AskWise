from django.db import models

class register(models.Model):
    fname=models.TextField(nulls=True)
    lname=models.TextField(nulls=True)
    
