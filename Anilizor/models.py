from django.contrib.auth.models import User
from django.db import models

class Docs(models.Model):
    name = models.CharField(max_length=255)  # Название документа
    file_path = models.FilePathField(path="/path/to/files")  # Путь к файлу
    size = models.IntegerField()  # Размер файла в байтах


    def __str__(self):
        return self.name

class Users_to_docs(models.Model):
    username = models.CharField(max_length=255)
    docs_id = models.ForeignKey(Docs, on_delete=models.CASCADE)

    def __str__(self):
        return self.username

class Prise(models.Model):
    file_type = models.CharField(unique=True)
    price = models.FloatField()

    def __str__(self):
        return self.file_type


class Cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    docs_id = models.ForeignKey(Docs, on_delete=models.CASCADE)
    order_price = models.FloatField()
    payment = models.BooleanField()

    def __str__(self):
        return self.user_id.username
