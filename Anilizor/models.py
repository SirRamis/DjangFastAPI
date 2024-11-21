from django.db import models

class Docs(models.Model):
    name = models.CharField(max_length=255)  # Название документа
    file_path = models.FilePathField(path="/path/to/files")  # Путь к файлу
    size = models.IntegerField()  # Размер файла в байтах


    def __str__(self):
        return self.name
