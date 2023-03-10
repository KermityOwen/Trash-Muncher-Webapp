from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.template.loader import render_to_string


from typing import List, Optional
from django.utils import timezone


class User(AbstractUser):
    is_player = models.BooleanField(default=False)
    is_gamekeeper = models.BooleanField(default=False)
    pass


class Team(models.Model):
    TEAMS = [("R", "Red"), ("B", "Blue"), ("G", "Green")]
    name = models.CharField(max_length=10)
    points = models.IntegerField(default=0)


class Player(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="player",
    )
    team = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL)


class GameKeeper(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="gamekeeper",
    )


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):
    """
    Handles password reset tokens. Once created, sends an email to the user
    :param sender: View Class that sent the email
    :param instance: View Instace that sent the signal
    :param reset_password_token: Token Model Object
    """

    email_plaintext_message = "{}?token={}".format(
        reverse("password_reset:reset-password-request"), reset_password_token.key
    )

    send_mail(
        subject="Password Reset for {title}".format(title="Trashmunchers"),
        message=email_plaintext_message,
        from_email="noreply@localhost",  # Needs to be changed https://studygyaan.com/django/how-to-send-email-in-django
        recipient_list=[reset_password_token.user.email],
    )
