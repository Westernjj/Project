from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta
import random

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f'Profile({self.user.username})'


class VerificationCode(models.Model):
    PURPOSE_CHOICES = (('activation', 'activation'),)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='verification_codes')
    code = models.CharField(max_length=6)
    #purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES, default='activation')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    attempts = models.PositiveIntegerField(default=0)

    class Meta:
        indexes = [models.Index(fields=['user', 'purpose', 'is_used'])]

    def __str__(self):
        return f'{self.purpose} code for {self.user}'

    @staticmethod
    def generate_code():
        return f'{random.randint(0, 999999):06d}'

    @classmethod
    def issue(cls, user, ttl_minutes=15):
        # інвалідовуємо попередні невикористані
        cls.objects.filter(user=user, purpose='activation', is_used=False).update(is_used=True)
        return cls.objects.create(
            user=user,
            code=cls.generate_code(),
            purpose='activation',
            expires_at=timezone.now() + timedelta(minutes=ttl_minutes),
        )

    def is_valid(self, value):
        if self.is_used or timezone.now() > self.expires_at:
            return False
        return self.code == value