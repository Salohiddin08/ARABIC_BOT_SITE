from django.db import models
from datetime import timedelta, datetime
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    verification_code = models.CharField(max_length=6, null=True, blank=True)
    code_expiration = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def set_verification_code(self):
        from random import randint
        self.verification_code = str(randint(100000, 999999))
        self.code_expiration = datetime.now() + timedelta(minutes=1)
        self.save()
