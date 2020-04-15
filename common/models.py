from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    age = models.SmallIntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    def __str__(self):
        return self.user.username
