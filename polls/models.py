from django.db import models


class Gift1_History(models.Model):
    a = models.IntegerField()

class Gifts(models.Model):
    name = models.CharField(max_length=10)
    description = models.CharField(max_length=10)

