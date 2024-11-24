from django.contrib.auth.models import User
from django.db import models

class Docs(models.Model):
    name = models.CharField(max_length=255)  # Название документа
    file_path = models.FileField(upload_to='docs/')  # Путь к файлу
    size = models.IntegerField(blank=True, null=True)  # Размер файла в байтах


    def __str__(self):
        return self.name

class Users_to_docs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    docs_id = models.ForeignKey(Docs, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.docs_id.name}'

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

from django.db import models

class Image(models.Model):
    name = models.CharField(max_length=255)
    image_file = models.ImageField(upload_to='images/')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

