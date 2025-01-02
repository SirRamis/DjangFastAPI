from django.contrib.auth.models import User
from django.db import models

class Docs(models.Model):
    filename = models.CharField(max_length=255)
    file_path = models.FileField(upload_to='docs/')
    size = models.IntegerField(blank=True, null=True)

class Documents(models.Model):
    filename = models.CharField(max_length=255)
    file_path = models.FileField(upload_to='images/')
    size = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'documents'
        #managed = False  # Django не управляет этой таблицей


class DocumentsText(models.Model):
    id = models.AutoField(primary_key=True)
    document = models.ForeignKey(
        Documents,
        on_delete=models.CASCADE,
        related_name='document_texts'
    )  # Используем ForeignKey для связи с таблицей Documents
    text = models.TextField()

    class Meta:
        db_table = 'documents_text'
        #managed = False  # Django не управляет этой таблицей


class Users_to_docs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    docs_id = models.ForeignKey(Documents, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.docs_id.name}'

class Prise(models.Model):
    file_type = models.CharField(unique=True)
    price = models.FloatField()

    def __str__(self):
        return self.file_type


class Cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    docs_id = models.ForeignKey(Documents, on_delete=models.CASCADE)
    order_price = models.FloatField()
    payment = models.BooleanField()

    def __str__(self):
        return self.user_id.username

class Image(models.Model):
    name = models.CharField(max_length=255)
    image_file = models.ImageField(upload_to='images/')
    size = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

class Image1(models.Model):
    filename = models.CharField(max_length=255)
    file_path = models.ImageField(upload_to='images/')
    size = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Устанавливаем размер файла перед сохранением
        if self.file_path:
            self.size = self.file_path.size
        super().save(*args, **kwargs)  # Вызываем метод родительского класса для сохранения