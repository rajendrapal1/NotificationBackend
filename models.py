from django.db import models
from django.contrib.auth.models import User


class Trigger(models.Model):

    name = models.CharField( max_length=100,unique=True)

    description = models.TextField( blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class NotificationTemplate(models.Model):

    CHANNEL_CHOICES = [
        ("whatsapp", "WhatsApp"),
        ("email", "Email"),
        ("web_push", "Web Push"),
    ]

    trigger = models.ForeignKey(
        Trigger,
        on_delete=models.CASCADE,
        related_name="templates"
    )

    channel = models.CharField(
        max_length=20,
        choices=CHANNEL_CHOICES
    )

    name = models.CharField(
        max_length=150
    )

    subject = models.CharField(
        max_length=255,
        blank=True
    )

    body = models.TextField()

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=["trigger", "channel"],
                name="unique_trigger_channel"
            )
        ]

        ordering = ["trigger", "channel"]

    def __str__(self):
        return f"{self.trigger.name} - {self.channel}"


class UserDevice(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="devices"
    )

    subscription_id = models.CharField(
        max_length=255,
        unique=True
    )

    endpoint = models.TextField(
        blank=True
    )

    device_type = models.CharField(
        max_length=50,
        default="web"
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.device_type}"


class NotificationLog(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("sent", "Sent"),
        ("failed", "Failed"),
    ]

    CHANNEL_CHOICES = [
        ("whatsapp", "WhatsApp"),
        ("email", "Email"),
        ("web_push", "Web Push"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notification_logs"
    )

    trigger = models.ForeignKey(
        Trigger,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notification_logs"
    )

    template = models.ForeignKey(
        NotificationTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notification_logs"
    )

    channel = models.CharField(
        max_length=20,
        choices=CHANNEL_CHOICES
    )

    recipient = models.CharField(
        max_length=255
    )

    subject = models.CharField(
        max_length=255,
        blank=True
    )

    message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    provider_response = models.TextField(
        blank=True
    )

    error_message = models.TextField(
        blank=True
    )

    sent_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.channel} - "
            f"{self.status}"
        )