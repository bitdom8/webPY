from django import forms
from .models import *
from django.forms import ClearableFileInput
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import CaptchaField



class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=5)
    file = forms.FileField()

def handle_uploaded_file(f):
	with open('some/file/name.txt', 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)


class FileFieldForm(forms.Form):
	file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
	

class ModelFormWithFileField(models.Model):
	# file will be uploaded to MEDIA_ROOT/uploads
	upload = models.FileField(upload_to='uploads/')
	# or...
	# file will be saved to MEDIA_ROOT/uploads/2015/01/30
	upload = models.FileField(upload_to='uploads/%Y/%m/%d/')
	


