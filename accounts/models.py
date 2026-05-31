from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    pass


class Hobby(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Profile(models.Model):

    class GenderChoices(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        NON_BINARY = "NB", "Non-binary"
        AGENDER = "AG", "Agender"
        GENDERFLUID = "GF", "Genderfluid"
        GENDERQUEER = "GQ", "Genderqueer"
        BIGENDER = "BG", "Bigender"
        DEMIBOY = "DB", "Demiboy"
        DEMIGIRL = "DG", "Demigirl"
        TRANS_MAN = "TM", "Trans Man"
        TRANS_WOMAN = "TW", "Trans Woman"
        INTERSEX = "IX", "Intersex"
        OTHER = "OT", "Other"
        PREFER_NOT_TO_SAY = "PN", "Prefer not to say"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    display_name = models.CharField(max_length=50, blank=True)
    profile_picture_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)

    age = models.IntegerField(
        validators=[
            MinValueValidator(13),
            MaxValueValidator(110),
        ]
    )

    gender = models.CharField(
        choices=GenderChoices.choices,
        max_length=2,
    )

    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)

    hobbies = models.ManyToManyField(
        Hobby,
        blank=True,
        related_name="profiles",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.display_name or self.user.username


class Follow(models.Model):

    # Store follower metadata here.

    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following_relationships",
    )

    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower_relationships",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"],
                name="unique_follow_relationship",
            )
        ]

    def __str__(self):
        return f"{self.follower} -> {self.following}"
