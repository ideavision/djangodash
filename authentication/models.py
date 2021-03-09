from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = PhoneNumberField('Phone Number', unique=True,blank=False)
    group_name = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username
