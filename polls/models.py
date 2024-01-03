from django.db import models
from django.contrib.postgres.fields import ArrayField


class Gift1_History(models.Model):
    a = models.IntegerField()


class Gifts(models.Model):
    name = models.CharField()
    description = models.CharField()


class Board(models.Model):
    size = models.IntegerField()
    name = models.CharField()
    users_id = ArrayField(
        models.IntegerField(blank=True),
    )

