from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import random


class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.otp:
            self.otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        return super().save(*args, **kwargs)
    @property
    def expired(self):
        return timezone.now() > self.created + timezone.timedelta(minutes=20)
