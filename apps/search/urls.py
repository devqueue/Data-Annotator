from django.urls import path
from . import views


urlpatterns = [
    path('', views.classification, name="classification"),
    path('ner', views.ner, name="ner"),
    path('export', views.export, name="export"),
]
