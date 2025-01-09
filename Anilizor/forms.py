from django import forms
from .models import Image, Documents, Image1
from django.contrib.auth.models import User

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

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "password"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Password do not match")