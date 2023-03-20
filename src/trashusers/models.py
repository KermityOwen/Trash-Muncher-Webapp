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
    """
    Creates an User table in the database

    Attributes:
    email (django.db.models.EmailField): Email that the user used when signing up
    is_player (django.db.models.BooleanField): Field to confirm whether a user is a player
    is_gamekeeper (django.db.models.BooleanField): Field to confirm whether a user is a gamekeeper
    """

    email = models.EmailField(blank=False, unique=True)
    is_player = models.BooleanField(default=False)
    is_gamekeeper = models.BooleanField(default=False)
    pass


class Team(models.Model):
    """
    Creates a Team table in the database

    Attributes:
    TEAMS (list): List of the possible teams that the user can be. Each element is a tuple of the team's name and its abbreviation
    name (django.db.models.CharField): Name of the team. Cannot be more than 10 characters
    points (django.db.models.IntegerField): Number of points the team has accummulated
    """

    TEAMS = [("R", "Red"), ("B", "Blue"), ("G", "Green")]
    name = models.CharField(max_length=10)
    points = models.IntegerField(default=0)


class Player(models.Model):
    """
    Creates a Player table in the database

    Attributes:
    user (django.db.models.OneToOneField): Account that the player belongs to
    team (django.db.models.ForeignKey): The team that player belongs to
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="player",
    )
    team = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL)


class GameKeeper(models.Model):
    """
    Creates a Player table in the database

    Attributes:
    user (django.db.models.OneToOneField): Account that the player belongs to
    """

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
    Handles password reset tokens. Once created, sends an email to the user with a link to reset their passsword
    Parameters:
    sender (view) -  View Class that sent the email
    instance (instance) - View Instace that sent the signal
    reset_password_token (password_token) - Token Model Object
    """
    link = "{}?token={}".format(
        "trashmunchers.co.uk/reset-password", reset_password_token.key
    )
    email_plaintext_message = \
    """ 
        Hi {},

        There was a request to change your password!

        If you did not make this request then please ignore this email.

        Otherwise, please click this link to change your password: {}
    """.format(reset_password_token.user.username, link)

    send_mail(
        subject="Password Reset for {title}".format(title="Trashmunchers"),
        message=email_plaintext_message,
        from_email="noreply@trashmunchers.co.uk",
        recipient_list=[reset_password_token.user.email],
    )
