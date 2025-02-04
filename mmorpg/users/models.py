import random
import string
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now, timedelta

def generate_verification_code():
    """Generate verification code"""
    return ''.join(random.choices(string.digits, k=6))  

class EmailVerificationCode(models.Model):
    """Model for storing verification codes"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, default=generate_verification_code)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return now() > self.created_at + timedelta(minutes=10) 
