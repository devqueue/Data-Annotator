from django.urls import path
from . import views


urlpatterns = [
    path('', views.classification_view, name="classification"),
    path('ner', views.ner, name="ner"),
    path('export', views.export, name="export"),
]
