from django.urls import path, include
from . import views

# app_name = "uploadapi"

urlpatterns = [
    path('upload', views.upload_file, name="upload"),
    path('compute', views.compute, name="compute"),
    path('uploadapi',views.UploadView.as_view()),
]
