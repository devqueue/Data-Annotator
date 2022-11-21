from django.contrib import admin
from .models import Sentance, Classification, NER
# Register your models here.
admin.site.register([Sentance, Classification, NER])
