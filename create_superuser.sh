#!/bin/sh

python manage.py makemigrations
python manage.py migrate

if ! python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists()"; then
    echo "Создание суперпользователя..."
    python manage.py createsuperuser --noinput --username "admin" --email "admin@admin.com"
else
    echo "Суперпользователь уже существует"
fi

python manage.py shell -c "
from django.contrib.auth import get_user_model;
User  = get_user_model();
user = User.objects.get(username='admin');
user.set_password('admin');
user.save();
"

python manage.py runserver 0.0.0.0:8011