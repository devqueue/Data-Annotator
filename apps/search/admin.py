from django.contrib import admin
from .models import Sentance_for_classification, Sentance_for_tagging, Classification, NER
# Register your models here.
admin.site.register([Sentance_for_classification, Sentance_for_tagging, Classification, NER])
