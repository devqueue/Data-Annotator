from django.db import models

# Create your models here.

class LABELS(models.IntegerChoices):
    TRUE = 1
    FALSE = 0


class Sentance_for_classification(models.Model):
    id = models.IntegerField(primary_key=True)
    sentance = models.TextField()
    classified_by = models.TextField()

class Sentance_for_tagging(models.Model):
    id = models.IntegerField(primary_key=True)
    sentance = models.TextField()
    tagged_by = models.TextField()


class Classification(models.Model):
    id = models.IntegerField(primary_key=True)
    sentance = models.TextField()
    label = models.IntegerField(choices=LABELS.choices)

class NER(models.Model):
    id = models.AutoField(primary_key=True)
    sentance = models.IntegerField()
    word = models.TextField()
    tag = models.TextField()
