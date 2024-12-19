from django import forms
from .models import Image, Documents, Image1


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['name', 'image_file']

class FileUploadForm(forms.Form):
    file = forms.FileField()

class ImageUploadForm(forms.Form):
    file = forms.ImageField(label='Select an image', required=True)

class ImUpFor(forms.ModelForm):
    class Meta:
        model = Image1
        fields = ['filename']
