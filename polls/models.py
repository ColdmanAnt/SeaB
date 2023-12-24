from django.db import models


class Gift1_History(models.Model):
    a = models.IntegerField()

class Gifts(models.Model):
    name = models.CharField()
    description = models.CharField()

