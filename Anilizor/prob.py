import requests
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
FASTAPI_URL = "http://localhost:8000/get_doc"  # Используйте правильный URL

def fastapi():
    response = requests.get(FASTAPI_URL)
    if response.status_code == 200:
        result = response.json()
        print(f"Ответ от FastAPI: {result}")
        return result
    else:
        print(f"Ошибка: {response.status_code}")
        return {"error": response.text}

# Пример использования
result = fastapi()
print(result)
@login_required
def add_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = form.cleaned_data['image_file']
            files = {'file': image_file}
            response = requests.post(FASTAPI_URL, files=files)
            image = form.save()
            file_path = image.image_file.path
            if response.status_code == 200:
                message = response.json()
                file_path = message.get('file_path')
                filename = message.get('filename')
                document = Documents.objects.create(
                    filename=filename,
                    file_path=file_path,
                    size=image_file.size
                )
                logging.info(f"Filename: {filename}, File path: {file_path}")

                Users_to_docs.objects.create(user=request.user, docs_id=document)
            else:
                message = "Фиаско"
            return render(request, 'result.html', {'message': message})
        else:
            return render(request, 'result.html', {'form': form, 'message': 'Фиаско'})
    else:
        form = ImageForm()
    return render(request, 'add_image.html', {'form': form})