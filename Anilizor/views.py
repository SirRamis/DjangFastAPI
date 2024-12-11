from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Documents,DocumentsText
from django.contrib import messages
from .forms import ImageForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests

@login_required
def add_image(request):
    FASTAPI_URL = "http://localhost:8000/upload_doc/"
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

                return render(request, 'result.html', {"status": 'Файл успешно загружен'})
            else:
                return render(request, 'result.html', {"status": "Ошибка загрузки в FastAPI"})

    else:
        form = ImageForm()
    return render(request, 'add_image.html', {'form': form})

def home1(request):
    return render(request, 'home1.html')

def base1(request):
    return render(request, 'base1.html')




@login_required
def show_images(request):
    FASTAPI_URL = "http://localhost:8000/get_doc"
    response = requests.get(FASTAPI_URL)
    app_folder = 'C:\\Users\\Ramis\\PycharmProjects\\DjangFastAPI\\media'
    #app_folder = settings.MEDIA_ROOT

    docu = Documents.objects.filter(file_path__isnull=False, file_path__startswith=app_folder)
    #docu = Documents.objects.filter(file_path__isnull=False, file_path__startswith=app_folder)

    if response.status_code == 200:
        for document in docu:
            document.analysis_price = f'{(document.size or 0) * 0.001:.2f}'
        return render(request, 'show_images.html', {'images': docu})
    else:
        print(f"Ошибка: {response.status_code}")
        # Возвращаем HttpResponse вместо множества
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

def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('login')  # Перенаправление на страницу входа после выхода

def about(request):
    return render(request, 'about.html')

def is_moderator_or_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

@login_required
def delete_doc(request):
    if not is_moderator_or_admin(request.user):
        return render(request, 'not_moder.html')
    if request.method == "POST":
        doc_id = request.POST.get("doc_id")
        if not doc_id:
            return HttpResponse("ID документа не указан", status=400)
        try:
            response = requests.delete(f"http://localhost:8000/delete_doc/{doc_id}")
            if response.status_code == 200:
                return render(request, 'delete_mess.html', {'message':"Успешно удалено."})
            else:
                return render(request, 'delete_mess.html', {'message':"Произошла ошибка."})
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
            response = requests.post(f"http://localhost:8000/doc_analyse/{document_id}")
            if response.status_code == 200:
                # document_id = 25
                FASTAPI_URL = f"http://localhost:8000/doc_text/{document_id}"
                FAST_URL = f"http://localhost:8000/doc_text"
                analysis_result = response.json()
                analyzed_text = analysis_result.get("text", "Текст отсутствует")
                gettext = DocumentsText.objects.all()
                print(gettext)
                #response = requests.get(FASTAPI_URL)
                # print(response)
                #return HttpResponse("Документ успешно проанализирован")
                return render(request, 'show_fanks.html', {'gettext': gettext})
                #return render(request, 'show_text.html', {'gettext': gettext})
            else:
                return HttpResponse(f"Ошибка при анализе документа")
        except Exception as e:
            return HttpResponse(f"Произннношла ошибка: {e}", status=500)
    documents = Documents.objects.all()
    return render(request, "analyze_image.html", {"documents": documents})

def show_fanks(request):
    gettext = DocumentsText.objects.all()
    return render(request, 'show_text.html', {'gettext': gettext})
def show_text(request):
    FASTAPI_URL = f"http://localhost:8000/get_text"
    response = requests.get(FASTAPI_URL)
    if response.status_code == 200:
        getext = DocumentsText.objects.all()
        fastapi_data = response.json()
        analyzed_text = fastapi_data.get("text", "Текст отсутствует")
        return render(request, 'show_text.html', {'gettext': getext})
    else:
        analyzed_text = f"Ошибка FastAPI: {response.status_code}"
    return render(request, 'show_text.html', {'analyzed_text': analyzed_text})


@csrf_exempt
def payment(request):
    is_payment_successful = True
    if is_payment_successful:
        return render(request, 'payment.html')
    else:
        return HttpResponse(f'<h2>Оплата не прошла</h2>')


# @login_required
# def show_results(request):
#     documents = DocumentsText.objects.filter(user=request.user)
#     return render(request, 'results.html', {'documents': documents})