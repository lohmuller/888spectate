from collections.abc import Iterable
from typing import Any, Coroutine
from django.db import models, connection
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class Sport(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Event(models.Model):

    class Meta:
        app_label = 'spectate'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    active = models.BooleanField(default=True)
    type = models.CharField(max_length=20, choices=[(
        'preplay', 'Preplay'), ('inplay', 'Inplay')])
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), (
        'Started', 'Started'), ('Ended', 'Ended'), ('Cancelled', 'Cancelled')])
    scheduled_start = models.DateTimeField()
    actual_start = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Selection(models.Model):

    class Meta:
        app_label = 'spectate'

    name = models.CharField(max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)
    outcome = models.CharField(max_length=20, choices=[(
        'Unsettled', 'Unsettled'), ('Void', 'Void'), ('Lose', 'Lose'), ('Win', 'Win')])

    def __str__(self):
        return self.name
