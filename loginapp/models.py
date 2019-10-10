import os
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='images/profile_pictures/')
    key = models.TextField(max_length=282)

    def __str__(self):
        return f"{self.user}"