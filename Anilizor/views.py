from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from time import sleep
from .models import Docs, Users_to_docs, Documents
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import Image
from .forms import ImageForm, ImageUploadForm
from django.contrib.auth.decorators import login_required, user_passes_test
import requests
import logging

#ручки для фаст апи
FASTAPI_URL = "http://localhost:8000/upload_doc/"  # Адрес FastAPI
# views.py

# def add_image(request):
#     if request.method == 'POST' and request.FILES['file']:
#         file = request.FILES['file']
#         files = {'file': file}
#         response = requests.post(FASTAPI_URL, files=files)
#         if response.status_code == 200:
#             message = "Успешно"
#         else:
#             message = "Фиаско"
#         return render(request, 'result.html', {'message': message})
#     return render(request, 'add_image.html')
# @login_required
# def add_image(request):
#     if request.method == 'POST':
#         form = ImageForm(request.POST, request.FILES)
#         if form.is_valid():
#             image_file = form.cleaned_data['image_file']
#             files = {'file': image_file}
#             response = requests.post(FASTAPI_URL, files=files)
#             image = form.save()
#             file_path = image.image_file.path
#             if response.status_code == 200:
#                 message = response.json()
#                 file_path = message.get('file_path')
#                 filename = message.get('filename')
#                 document = Documents.objects.create(
#                     filename=filename,
#                     file_path=file_path,
#                     size=image_file.size
#                 )
#                 logging.info(f"Filename: {filename}, File path: {file_path}")
#
#                 Users_to_docs.objects.create(user=request.user, docs_id=document)
#             else:
#                 message = "Фиаско"
#             return render(request, 'result.html', {'message': message})
#         else:
#             return render(request, 'result.html', {'form': form, 'message': 'Фиаско'})
#     else:
#         form = ImageForm()
#     return render(request, 'add_image.html', {'form': form})


@login_required
def add_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            file_path = image.image_file.path
            print(f"Загружаем файл: {file_path}")
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(FASTAPI_URL, files=files)
            print(f"Ответ FastAPI: {response.status_code} - {response.text}")
            if response.status_code == 200:
                api_result = response.json()
                status = api_result.get("status", "Неизвестный статус")
                filename = api_result.get("filename", "Неизвестное имя файла")

                document = Documents.objects.create(
                    filename=filename,
                    file_path=file_path,
                    size=image.image_file.size
                )

                return render(request, 'result.html', {"status": status})
            else:
                return render(request, 'result.html', {"status": "Ошибка загрузки в FastAPI"})

    else:
        form = ImageForm()
    return render(request, 'add_image.html', {'form': form})

def home1(request):
    documents = Docs.objects.all()
    return render(request, 'home1.html')

def base1(request):
    return render(request, 'base1.html')
# @login_required
# def show_images(request):
#     documents = Documents.objects.all()
#     return render(request, 'show_images.html', {'documents': documents})
#
# @login_required
# def show_images(request):
#     image = Documents.objects.all()
#     return render(request, 'show_images.html', {'images': image})
# @login_required
# def show_images(request):
#     image = Image.objects.all()
#     return render(request, 'show_images.html', {'images': image})
@login_required
def show_images(request):
    FASTAPI_URL = "http://localhost:8000/get_doc"
    response = requests.get(FASTAPI_URL)
    docu = Documents.objects.filter(file_path__isnull=False)
    if response.status_code == 200:
        result = response.json()
        # print(f"Ответ от FastAPI: {result}")
        # images = result['files']
        # image_urls = [f"/media/{image['filename']}" for image in images]
        return render(request, 'show_images.html', {'images': docu})
    else:
        print(f"Ошибка: {response.status_code}")
        return {"error": response.text}

def analyze_image(request, image_id):
    image = Image.objects.get(id=image_id)
    result = f"Анализ {image.name} успешно."
    return JsonResponse({'message': result})


# # Регистрация
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

# Вход
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

# Выход
def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('login')  # Перенаправление на страницу входа после выхода

def about(request):
    return render(request, 'about.html')

def is_moderator_or_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

@login_required
#@user_passes_test(is_moderator_or_admin)
def delete_doc(request):
    if request.method == "POST":
        doc_id = request.POST.get("doc_id")
        if not doc_id:
            return HttpResponse("ID документа не указан", status=400)
        try:
            response = requests.post(
                "http://127.0.0.1:8000/delete_doc",
                json={"doc_id": int(doc_id)},
            )
            if response.status_code == 200:
                return HttpResponse("Документ успешно удален")
            else:
                return HttpResponse(f"Ошибка при удалении документа")
        except Exception as e:
            return HttpResponse(f"Произошла ошибка: {e}", status=500)
    return render(request, "delete_doc.html")