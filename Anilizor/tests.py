from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Documents,DocumentsText
from django.urls import reverse

#python manage.py test



class TestAnilizorPage(TestCase):

    def test_base(self):
        response = self.client.get("/base1/")
        self.assertEqual(response.status_code, 200)

    def test_payment(self):
        response = self.client.get("/payment/")
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200)

class TestModelDocuments(TestCase):
    def test_create_document(self):
        document = Documents.objects.create(
            filename="example.txt",
            file_path="/path/to/example.txt",
            size=12345
        )
        self.assertEqual(document.filename, "example.txt")
        self.assertEqual(document.file_path, "/path/to/example.txt")
        self.assertEqual(document.size, 12345)
class TesShowImages(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client = Client()
        self.document = Documents.objects.create(
            filename="example.txt",
            file_path="/path/to/example.txt",
            size=12345
        )
    def test_show_images(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse('show_images'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_images.html')