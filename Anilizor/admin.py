from django.contrib import admin
from .models import Prise

@admin.register(Prise)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('file_type', 'price')

# @admin.register(Prise)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('file_type', 'price')