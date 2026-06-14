from datetime import date
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    MinLengthValidator,
    URLValidator,
)
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Hobby(models.Model):

    class HobbyChoices(models.TextChoices):
        READING = "READING", "Reading"
        WRITING = "WRITING", "Writing"
        GAMING = "GAMING", "Gaming"
        PROGRAMMING = "PROGRAMMING", "Programming"
        WEB_DEV = "WEB_DEV", "Web Development"
        AI = "AI", "Artificial Intelligence"
        DATA_SCIENCE = "DATA_SCIENCE", "Data Science"

        CHESS = "CHESS", "Chess"
        BOARD_GAMES = "BOARD_GAMES", "Board Games"
        PUZZLES = "PUZZLES", "Puzzle Solving"

        COOKING = "COOKING", "Cooking"
        BAKING = "BAKING", "Baking"

        PHOTOGRAPHY = "PHOTOGRAPHY", "Photography"
        VIDEOGRAPHY = "VIDEOGRAPHY", "Videography"

        DRAWING = "DRAWING", "Drawing"
        PAINTING = "PAINTING", "Painting"
        DIGITAL_ART = "DIGITAL_ART", "Digital Art"
        GRAPHIC_DESIGN = "GRAPHIC_DESIGN", "Graphic Design"

        MUSIC = "MUSIC", "Music"
        SINGING = "SINGING", "Singing"
        GUITAR = "GUITAR", "Playing Guitar"
        PIANO = "PIANO", "Playing Piano"

        DANCING = "DANCING", "Dancing"
        ACTING = "ACTING", "Acting"

        MOVIES = "MOVIES", "Watching Movies"
        TV_SHOWS = "TV_SHOWS", "Watching TV Shows"
        ANIME = "ANIME", "Anime"
        MANGA = "MANGA", "Manga"

        BLOGGING = "BLOGGING", "Blogging"
        PODCASTING = "PODCASTING", "Podcasting"

        TRAVEL = "TRAVEL", "Traveling"
        HIKING = "HIKING", "Hiking"
        CAMPING = "CAMPING", "Camping"

        FITNESS = "FITNESS", "Fitness"
        RUNNING = "RUNNING", "Running"
        CYCLING = "CYCLING", "Cycling"
        SWIMMING = "SWIMMING", "Swimming"
        YOGA = "YOGA", "Yoga"

        FOOTBALL = "FOOTBALL", "Football"
        BASKETBALL = "BASKETBALL", "Basketball"
        TENNIS = "TENNIS", "Tennis"

        SKIING = "SKIING", "Skiing"
        SNOWBOARDING = "SNOWBOARDING", "Snowboarding"

        FASHION = "FASHION", "Fashion"
        MAKEUP = "MAKEUP", "Makeup"

        INVESTING = "INVESTING", "Investing"
        CRYPTO = "CRYPTO", "Cryptocurrency"

        LANGUAGES = "LANGUAGES", "Learning Languages"
        PHILOSOPHY = "PHILOSOPHY", "Philosophy"
        PSYCHOLOGY = "PSYCHOLOGY", "Psychology"

        VOLUNTEERING = "VOLUNTEERING", "Volunteering"
        PETS = "PETS", "Pets"

    name = models.CharField(
        max_length=50,
        unique=True,
        choices=HobbyChoices.choices,
    )

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

    display_name = models.CharField(
        max_length=50,
        blank=True,
        validators=[MinLengthValidator(2)],
    )

    profile_picture_url = models.URLField(
        blank=True,
        validators=[URLValidator()],
    )

    bio = models.TextField(
        blank=True,
        max_length=500,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    gender = models.CharField(
        choices=GenderChoices.choices,
        max_length=2,
        blank=True,
        default=GenderChoices.PREFER_NOT_TO_SAY,
    )

    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)

    hobbies = models.ManyToManyField(
        Hobby,
        blank=True,
        related_name="profiles",
    )

    instagram = models.CharField(max_length=30, blank=True)
    twitter = models.CharField(max_length=30, blank=True)
    facebook = models.CharField(max_length=100, blank=True)
    tiktok = models.CharField(max_length=30, blank=True)
    youtube = models.CharField(max_length=100, blank=True)

    discord_username = models.CharField(
        max_length=100,
        blank=True,
        help_text="e.g. username or username#1234 (legacy)",
    )

    github = models.CharField(max_length=50, blank=True)
    linkedin = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_public = models.BooleanField(default=True)
    show_age = models.BooleanField(default=True)
    show_location = models.BooleanField(default=True)
    show_hobbies = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    last_seen = models.DateTimeField(null=True, blank=True)
    is_online = models.BooleanField(default=False)

    cantina_score = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    def clean(self):
        if self.last_seen and self.last_seen > timezone.now():
            raise ValidationError("last_seen cannot be in the future")

        if self.date_of_birth:
            today = date.today()
            age = (
                today.year
                - self.date_of_birth.year
                - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
            )

            if age < 13:
                raise ValidationError("User must be at least 13 years old.")

        if self.display_name and len(self.display_name.strip()) < 2:
            raise ValidationError("Display name too short.")

    def __str__(self):
        return self.display_name or self.user.username


class Follow(models.Model):

    class Status(models.TextChoices):
        FOLLOWING = "FOLLOWING", "Following"
        PENDING = "PENDING", "Pending"

    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following_set",
    )

    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followers_set",
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.FOLLOWING,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"],
                name="unique_follow",
            )
        ]


class Block(models.Model):
    blocker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blocking",
    )

    blocked = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blocked_by",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["blocker", "blocked"],
                name="unique_block",
            )
        ]

    def __str__(self):
        return f"{self.blocker} blocked {self.blocked}"


class ProfileComment(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="profile_comments",
    )

    text = models.TextField(max_length=1000)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author} -> {self.profile}"
