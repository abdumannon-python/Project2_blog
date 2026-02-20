from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class Emailcode(models.Model):
    users=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='code')
    code=models.CharField(max_length=6)
    created_at=models.DateTimeField(auto_now_add=True)
    def is_valid(self):
        return timezone.now()<self.created_at+timedelta(minutes=2)
    def __str__(self):
        return f" {self.users.username} uchun kod {self.code}"