from django.contrib.auth.models import User
from django.db import models
from django.contrib.postgres.fields import ArrayField


class Gift1_History(models.Model):# не нужно#
    a = models.IntegerField()


class Image(models.Model):# не нужно#
    Img = models.ImageField(upload_to='images/', default='images/gift_card.png')


class MyGifts(models.Model):
    user = models.IntegerField(default=1)
    name = models.CharField()
    description = models.CharField()
    Img = models.ImageField(upload_to='images/', default='images/gift_card.png')


class MyResults(models.Model):
    user = models.IntegerField()
    board_id = models.IntegerField()
    gifts_id = ArrayField(
        models.IntegerField(blank=True),
    )


class Gifts(models.Model):
    name = models.CharField()
    description = models.CharField()
    Img = models.ImageField(upload_to='images/', default='images/gift_card.png')


class GameBoard(models.Model):# не нужно#
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
        default=[]
    )


class Ship(models.Model):
    board_id = models.IntegerField()
    x = models.IntegerField()
    y = models.IntegerField()
    gift_id = models.IntegerField(default=1)
    winner_id = models.IntegerField(default=1)


class BoardAccess(models.Model):
    shots = models.IntegerField(default=2)
    us = models.IntegerField()
    board_id = models.IntegerField()
    start_shot = models.IntegerField()


class GiftWinners(models.Model):  # не нужно#
    gift_id = models.IntegerField()
    winner_id = models.IntegerField()


class MyShots(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    user_id = models.IntegerField()
    board_id = models.IntegerField(default=1)
