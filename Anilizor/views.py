import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from .models import Documents, DocumentsText, Image, Image1
from django.contrib import messages
from .forms import ImageForm, ImageForm1
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import requests

FASTAPI_HOST = 'http://host.docker.internal:8000'



def check_jwt_tokens(request):
    access_token = request.COOKIES.get("access")
    #logger.info(f"Access token from cookies: {access_token}")


    if access_token is None:
        refresh_token = request.COOKIES.get("refresh")
        if refresh_token is None:
            #logger.warning("No access or refresh token found, redirecting to login.")
            return redirect("login")

        try:
            response = requests.post(f"http://host.docker.internal:8090/refresh/", data={'refresh': refresh_token})
            response.raise_for_status()
            new_tokens = response.json()
            access_token = new_tokens.get("access")
            refresh_token = new_tokens.get("refresh")
            #logger.info(f"Access token refreshed successfully: {access_token}")
        except requests.exceptions.RequestException as e:
            #logger.error(f"Failed to refresh token: {str(e)}")
            return redirect("login")

    headers = {"Authorization": f"Bearer {access_token}"}
    #logger.info(f"Headers prepared for request: {headers}")
    return headers



"""Аутентификация и авторизация пользователя"""

class CustomLoginView(LoginView):
    template_name = "login.html"
    success_url = "base1.html"

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        response = super().form_valid(form)

        data = {"username": username, "password": password}

        jwt_response = requests.post(f"http://host.docker.internal:8090/api/token/", json=data)

        if jwt_response.status_code == 200:
            tokens = jwt_response.json()
            access_token = tokens["access"]
            refresh_token = tokens["refresh"]

            response.set_cookie('access', access_token, max_age=300)
            response.set_cookie('refresh', refresh_token, max_age=3600)

        else:
            response = JsonResponse({"error": f"Failed to obtain JWT token from API. {jwt_response.status_code}"}, status=500)
        return response



import requests

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Синхронизация с Django REST
            try:
                response = requests.post(
                    'http://host.docker.internal:8090/register/',
                    json={
                        'username': user.username,
                        'password': request.POST['password1'],
                    },
                )
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                messages.error(request, f"Ошибка синхронизации с REST API: {e}")
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('add_image')
        else:
            messages.error(request, 'Ошибка регистрации. Проверьте данные.')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})



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
def add_image(request):
    if request.method == 'POST':
        form = ImageForm1(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save()
            file_path = image_instance.file_path.path  # Путь к файлу
            file_name = image_instance.file_path.name  # Имя файла
            file_size = image_instance.file_path.size  # Размер файла
            headers = check_jwt_tokens(request)
            #headers = {"Authorization": f"Bearer {access_token}"}
            # Отправка изображения в другой сервис
            with open(file_path, 'rb') as file:

                files = {'file': image_instance.file_path}
                response = requests.post("http://host.docker.internal:8000/upload_doc/", files=files, headers=headers)

            if response.status_code == 200:
                return render(request, 'result.html', {"status": 'Файл успешно загружен'})
            else:
                return render(request, 'result.html',
                              {"status": "Файл успешно загружен!"})
    else:

        form = ImageForm1()
    return render(request, 'add_image.html', {'form': form})


@login_required
def show_images(request):
    headers = check_jwt_tokens(request)
    print(f'ТУТ ХЕДЕР : {headers}')
    response = requests.get("http://host.docker.internal:8090/show_images", headers=headers)
    if response.status_code == 200:
        docu = Image1.objects.all()
        for document in docu:
            document.analysis_price = f'{(document.size or 0) * 0.001:.2f}'
        return render(request, 'show_images.html', {'images': docu})
    else:
        return HttpResponse(f"Ошибка при обращении к FastAPI: {response.status_code}", status=500)



@login_required
def delete_doc(request):
    if not is_moderator_or_admin(request.user):
        return render(request, 'not_moder.html')
    if request.method == "POST":
        document_id = request.POST.get("doc_id")
        headers = check_jwt_tokens(request)
        print(f'ТУТ ХЕДЕР : {headers}')
        if not document_id:
            return HttpResponse("ID документа не указан", status=400)
        try:
            response = requests.delete(f"http://host.docker.internal:8090/delete/{document_id}", headers=headers)
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
        headers = check_jwt_tokens(request)
        if not document_id:
            return HttpResponse("ID документа не указан", status=400)
        try:
            response = requests.post(f"http://host.docker.internal:8090/analyse/{document_id}", headers=headers)
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


# def show_thanks(request):
#     gettext = DocumentsText.objects.all()
#     return render(request, 'show_text.html', {'gettext': gettext})
def show_thanks(request):
    return show_text()




@login_required
def show_text(request):
    headers = check_jwt_tokens(request)
    print(f'ТУТ ТОКЕН : {headers}')
    response = requests.get("http://host.docker.internal:8090/get_text", headers=headers)
    if response.status_code == 200:
        gettext = response.json()
        documents = gettext.get('documents', [])
        return render(request, 'show_text.html', {'gettext': documents})
    else:
        analyzed_text = f"Ошибка FastAPI: {response.status_code}"
    return render(request, 'show_text.html', {'analyzed_text': analyzed_text})
