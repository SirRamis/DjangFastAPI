from django import forms
from .models import Image, Documents, Image1


class ImageForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = ['filename', 'file_path']


class FileUploadForm(forms.Form):
    file = forms.FileField()


class ImageUploadForm(forms.Form):
    file = forms.ImageField(label='Select an image', required=True)


class ImageForm1(forms.ModelForm):
    class Meta:
        model = Image1
        fields = ['filename', 'file_path']
