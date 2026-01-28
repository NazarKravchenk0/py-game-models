from django.db import models
from django.utils import timezone


class Race(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True)
    bonus = models.CharField(max_length=255)
    race = models.ForeignKey(Race, on_delete=models.CASCADE,
                             related_name="skills")

    def __str__(self) -> str:
        return self.name


class Guild(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Player(models.Model):
    nickname = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255)  # non-unique by default
    bio = models.CharField(max_length=255)

    # Player must be deleted when Race is deleted
    race = models.ForeignKey(Race, on_delete=models.CASCADE,
                             related_name="players")

    # Player must NOT be deleted when Guild is deleted
    guild = models.ForeignKey(
        Guild,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="players",
    )

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.nickname
