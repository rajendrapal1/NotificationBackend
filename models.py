from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True
    )

    last_login_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username