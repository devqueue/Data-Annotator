from django.db import models

# Create your models here.

# todo: fetch users from table
USERS = []

class LABELS(models.IntegerChoices):
    TRUE = 1
    FALSE = 0
class TAGS(models.TextChoices):
    O = 'O'
    Object = 'Object'
    Attribute = 'Attribute'
    Function = 'Function'
    Operator = 'Operator'
    Value = 'Value'
    Unit = 'Unit'


class Sentance(models.Model):
    id = models.IntegerField(primary_key=True)
    sentance = models.TextField()
    classified_by = models.TextField()
    tagged_by = models.TextField()


class Classification(models.Model):
    id = models.IntegerField(primary_key=True)
    sentance = models.TextField()
    label = models.IntegerField(choices=LABELS.choices)

class NER(models.Model):
    id = models.IntegerField(primary_key=True)
    sentance = models.IntegerField()
    words = models.TextField()
    tag = models.TextField(choices=TAGS.choices)
