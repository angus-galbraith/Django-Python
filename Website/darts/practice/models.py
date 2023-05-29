from django.db import models

# Create your models here.
class rtbHighScore(models.Model):
    name = models.CharField(max_length=20)
    score = models.IntegerField()


class finishesHighScore(models.Model):
    name = models.CharField(max_length=20)
    score = models.IntegerField()