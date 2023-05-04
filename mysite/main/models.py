from unittest.util import _MAX_LENGTH
from django.db import models
from django import forms
from django.contrib.auth.models import User

# Create your models here.
class idModel(models.Model):
    username = models.CharField(max_length = 200)
    password = models.CharField(max_length = 200)
    school = models.CharField(max_length=200)
    def __str__(self):
            return self.sesid
