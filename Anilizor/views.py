from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Docs, Users_to_docs
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Image
from .forms import ImageForm
from django.contrib.auth.decorators import login_required

def home1(request):
    documents = Docs.objects.all()
    return render(request, 'home1.html')


def base1(request):
    return render(request, 'base1.html')
@login_required
def add_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()


            doc = Docs.objects.create(
                name=image.name,  # Имя файла
                file_path=image.image_file.path,  # Путь к файлу
                size=image.image_file.size  # Размер файла
            )
            Users_to_docs.objects.create(user=request.user, docs_id=doc)
            return redirect('show_images')
    else:
        form = ImageForm()
    return render(request, 'add_image.html', {'form': form})

@login_required
def show_images(request):
    images = Image.objects.all()
    return render(request, 'show_images.html', {'images': images})

def analyze_image(request, image_id):
    image = Image.objects.get(id=image_id)
    # Здесь будет логика анализа
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