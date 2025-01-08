import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.forms import Form

from DjangFastAPI import settings
from DjangFastAPI.settings import FASTAPI_URL
from .models import Documents, DocumentsText, Image, Image1
from django.contrib import messages
from .forms import ImageForm, ImageForm1
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests

FASTAPI_HOST = 'http://host.docker.internal:8000'

# def add_image(request):
#     if request.method == 'POST':
#         form = ImageForm1(request.POST, request.FILES)
#         if form.is_valid():
#             image_instance = form.save()
#             files = {'file': image_instance.file_path}
#             response = requests.post("http://host.docker.internal:8090/upload", files=files)
#         if response.status_code == 200:
#             return render(request, 'result.html')
#         else:
#             return render(request, 'result.html', {"status": "Файл успешно загружен!!!"})
#     else:
#         form = ImageForm1()
#     return render(request, 'add_image.html', {'form': form})
def add_image(request):
    if request.method == 'POST':
        form = ImageForm1(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save()
            file_path = image_instance.file_path.path  # Путь к файлу
            file_name = image_instance.file_path.name  # Имя файла
            file_size = image_instance.file_path.size  # Размер файла

            # Отправка изображения в другой сервис
            with open(file_path, 'r+b') as file:

                files = {'file': image_instance.file_path}
                response = requests.post("http://host.docker.internal:8000/upload_doc/", files=files)

            if response.status_code == 200:
                return render(request, 'result.html', {"status": 'Файл успешно загружен'})
            else:
                return render(request, 'result.html',
                              {"status": "Файл успешно загружен!"})
    else:
        print('ffffff')
        form = ImageForm1()
    return render(request, 'add_image.html', {'form': form})


@login_required
def show_images(request):
    response = requests.get("http://host.docker.internal:8090/show_images")
    if response.status_code == 200:
        docu = Image1.objects.all()
        for document in docu:
            document.analysis_price = f'{(document.size or 0) * 0.001:.2f}'
        return render(request, 'show_images.html', {'images': docu})
    else:
        return HttpResponse(f"Ошибка при обращении к FastAPI: {response.status_code}", status=500)


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('add_image')  # Перенаправление после регистрации
        else:
            messages.error(request, 'Ошибка регистрации. Проверьте данные.')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('base1')  # Перенаправление после входа
        else:
            messages.error(request, 'Неправильные имя пользователя или пароль.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@csrf_exempt
def payment(request):
    is_payment_successful = True
    if is_payment_successful:
        return render(request, 'payment.html')
    else:
        return HttpResponse(f'<h2>Оплата не прошла</h2>')


def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('login')  # Перенаправление на страницу входа после выхода


def about(request):
    return render(request, 'about.html')


def is_moderator_or_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def home1(request):
    return render(request, 'home1.html')


def base1(request):
    return render(request, 'base1.html')


@login_required
def delete_doc(request):
    if not is_moderator_or_admin(request.user):
        return render(request, 'not_moder.html')
    if request.method == "POST":
        doc_id = request.POST.get("doc_id")
        if not doc_id:
            return HttpResponse("ID документа не указан", status=400)
        try:
            response = requests.delete(f"http://host.docker.internal:8090/delete/{doc_id}")
            if response.status_code == 200:
                return render(request, 'delete_mess.html', {'message': "Успешно удалено."})
            else:
                return render(request, 'delete_mess.html', {'message': "Произошла ошибка."})
        except Exception as e:
            return HttpResponse(f"Произошла ошибка: {e}", status=500)
    return render(request, "delete_doc.html")


@login_required
def analyze_image(request, document_id):
    if request.method == "POST":
        document_id = request.POST.get("document_id")
        if not document_id:
            return HttpResponse("ID документа не указан", status=400)
        try:
            response = requests.post(f"http://host.docker.internal:8090/analyse/{document_id}")
            if response.status_code == 200:
                analysis_result = response.json()
                analyzed_text = analysis_result.get("text", "Текст отсутствует")
                #gettext = DocumentsText.objects.all()
                return render(request, 'show_thanks.html', {'gettext': analyzed_text})
            else:
                return HttpResponse(f"Ошибка при анализе документа")
        except Exception as e:
            return HttpResponse(f"Произннношла ошибка: {e}", status=500)
    documents = Documents.objects.all()
    return render(request, "analyze_image.html", {"documents": documents})


def show_thanks(request):
    gettext = DocumentsText.objects.all()
    return render(request, 'show_text.html', {'gettext': gettext})


def show_text(request):
    response = requests.get("http://host.docker.internal:8090/get_text")
    if response.status_code == 200:
        gettext = response.json()
        documents = gettext.get('documents', [])
        return render(request, 'show_text.html', {'gettext': documents})
    else:
        analyzed_text = f"Ошибка FastAPI: {response.status_code}"
    return render(request, 'show_text.html', {'analyzed_text': analyzed_text})
