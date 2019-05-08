from django.db import models
from notesystem.models import Notes


# Create your models here.
class FileModel(models.Model):
    file_path = models.FileField(upload_to='')
    file_attribution = models.CharField(max_length=255)
    file_name = models.CharField(max_length=256)
    file_owner = models.CharField(max_length=256)
    upload_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.file_name


