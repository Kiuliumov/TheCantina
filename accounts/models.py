from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


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

    name = models.CharField(max_length=50, unique=True, choices=HobbyChoices.choices)

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
    date_of_birth = models.DateField(null=True, blank=True)

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

    instagram = models.CharField(max_length=50, blank=True)
    twitter = models.CharField(max_length=50, blank=True)  # X handle
    facebook = models.CharField(max_length=100, blank=True)
    tiktok = models.CharField(max_length=50, blank=True)
    youtube = models.CharField(max_length=100, blank=True)

    discord_username = models.CharField(
        max_length=100, blank=True, help_text="e.g. username or username#1234 (legacy) or username"
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
    cantina_score = models.FloatField(default=0)

    def __str__(self):
        return self.display_name or self.user.username


class Follow(models.Model):

    class Status(models.TextChoices):
        FOLLOWING = "FOLLOWING", "Following"
        PENDING = "PENDING", "Pending"
        REQUESTED = "REQUESTED", "Requested"

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

        text = models.TextField()

        created_at = models.DateTimeField(auto_now_add=True)

        class Meta:
            ordering = ["-created_at"]

        def __str__(self):
            return f"{self.author} -> {self.profile}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    content_object = GenericForeignKey("content_type", "object_id")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "content_type", "object_id"],
                name="unique_like",
            )
        ]
