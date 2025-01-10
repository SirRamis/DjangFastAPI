"""
URL configuration for DjangFastAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Anilizor import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', views.home1),
                  path('about/', views.about, name='about'),
                  path('delete_doc/', views.delete_doc, name='delete_doc'),
                  path('base1/', views.base1, name='base1'),
                  path('register/', views.register_view, name='register'),
                  path('analyze_image/<int:document_id>/', views.analyze_image, name='analyze_image'),
                  path('login/', views.CustomLoginView.as_view(), name='login'),
                  path('logout/', views.logout_view, name='logout'),
                  path('add_image/', views.add_image, name='add_image'),
                  path('show_images/', views.show_images, name='show_images'),
                  path('show_text/', views.show_text, name='show_text'),
                  path('show_thanks/', views.show_thanks, name='show_thanks'),
                  path('payment/', views.payment, name='payment'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
