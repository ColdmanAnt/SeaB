from django.contrib.auth.models import User
from django.db import models
from django.contrib.postgres.fields import ArrayField


class Gift1_History(models.Model):
    a = models.IntegerField()


class Gifts(models.Model):
    name = models.CharField()
    description = models.CharField()


class GameBoard(models.Model):
    size = models.IntegerField()
    name = models.CharField()
    users_id = ArrayField(
        models.IntegerField(blank=True),
    )


class Board(models.Model):
    size = models.IntegerField()
    name = models.CharField()
    users_id = ArrayField(
        models.IntegerField(blank=True),
    )


class Ship(models.Model):
    board_id = models.IntegerField()
    x = models.IntegerField()
    y = models.IntegerField()
    gift_id = models.IntegerField(default=1)
    winner_id = models.ForeignKey(to=User, on_delete=models.CASCADE, default=1)


class BoardAccess(models.Model):
    shots = models.IntegerField(default=2)
    us = models.IntegerField()
    board_id = models.IntegerField()
