from django.db import models
from core.settings import UPLOAD_PATH
import os
# Create your models here.

class Csv(models.Model):
    id = models.AutoField(primary_key=True) 
    file_name = models.FileField()
    uploaded = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.file_name}"

    def delete(self, *args, **kwargs):
        filename = str(self.file_name)
        path = os.path.join(UPLOAD_PATH, filename)
        print(f"{filename} deleted")
        os.remove(path)
        super().delete(*args, **kwargs)
