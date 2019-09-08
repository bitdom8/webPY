from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from PIL import Image
from django import forms
from .models import *
from .forms import *
from django.core.validators import ValidationError
from ckeditor.fields import RichTextField
from betterforms.multiform import MultiModelForm
import datetime






def min_length_check(val):
	if len(val) <= 10:
		raise ValidationError("%(val) must be greater than 10", params={"val":val}
	
		)


class Contact(models.Model):
	name = models.CharField(max_length=125, null=True, default="1")
	email = models.EmailField(default="1")
	address = models.CharField(max_length=255,default="1")
	city = models.CharField(max_length=255,default="1")
	zipcode = models.CharField(max_length=255,default="")

	objects = models.Manager


# class Category(models.Model):
# 	title = models.CharField(validators = [min_length_check], max_length = 255)
# 	created_at = models.DateTimeField(auto_now_add = True)


# 	def __str__(self):
# 		return self.title
	
# 	class Meta:
# 		db_table = "category"
# 		verbose_name ="Category"
# 		verbose_name_plural = "Category"


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'author_{0}/{1}'.format(instance.author.id, filename)



# Create your models here.
class Post(models.Model):
	

	STATUS_CHOICES = {
		("draft", "Draft"),
		("published", "Published"),
	}
	

	author = models.ForeignKey(User, on_delete = models.CASCADE, default = 1 )
	title = models.CharField(max_length= 100, null=True, blank=True,  default="Başlık")
	content = models.TextField(blank =True, null=True, default = "Enter your content")
	image = models.ImageField(upload_to=user_directory_path, blank =True, null=True, default = "")
	date_posted = models.DateTimeField(default=timezone.now)
	document = models.FileField(upload_to='{{ {nop}  }}'.format(nop = "something"), default = "media/")
	thumbnail = models.FileField(upload_to='posts/', null = True, blank= True, default = "")
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
	# category = models.ManyToManyField(Category, default = 0)

	# thumbnail = models.FileField(upload_to='posts/'  gallery and thumbnail is different folders


	objects = models.Manager
	#it will show not <Question: Question object (1)> but the authors name or title

	def was_published_recently(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days=1)



	def get_absolute_url(self):
		return reverse("post-detail", kwargs={"pk": self.pk})

	def save(self, *args, **kwargs):
		self.slug = self.__str__()
		return super(Post, self).save(*args, **kwargs)



	def __str__(self):
		return "Başlık: "+ self.title + ", İçerik: " + self.content

# # new addded
# 	class Meta:  
# 		db_table = "posts"
# 		verbose_name = "Post"
# 		verbose_name_plural = "Posts"
class Gallery(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete = models.CASCADE, default = 1 )
	image = models.ImageField(upload_to=user_directory_path, blank =True, null=True, default = "/")

	content2 = models.TextField(blank =True, null=True, default = "/")

	objects = models.Manager

	def __str__(self):
		# self.image.path + 
		return self.image.url

class MyModel(models.Model):

	upload = models.FileField(upload_to='uploads/%Y/%m/%d/',default = "media/")

class PostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ["author", "title", "content", "image"]
		widgets = {
			"title": forms.TextInput(attrs={"class": "form-control"}),
			"thumbnail": forms.FileInput(attrs={"class": "form-control",
			"multiple": True}),
			"author": forms.Select(attrs={"class": "form-control"}),
			"image":  forms.FileInput(attrs={"class": "form-control",
			"multiple": True}),
			"document":forms.FileInput(attrs={"class": "form-control",
			"multiple": True}),
			# "category": forms.CheckboxSelectMultiple(attrs={"class":"list-unstyled list- inline"}),
		}
		help_texts = {
			"title": "Başlık girin | Enter title please",
			"content": "Ürünü detayla açıklayın | Express your product in detail",
		}
		error_messages = {

		}
		labels = {
			"author":"Yazar",
			"title": "Başlık",
			"content": "İçerik",
			"thumbnail": "Thumbnail",
		}
	def clean(self):
		fields = self.cleaned_data
		keys = list(fields.keys())
		print(fields)





	#not RELAVVANT!!!!

class Comment(models.Model):
	Post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = "comments")
	Content = models.TextField(verbose_name='Content', default="Başlık")
	Name = models.CharField(max_length = 100, default="Başlık")
	Email = models.EmailField(max_length = 100)
	Body = models.TextField()
	Created = models.DateTimeField(auto_now_add = True)
	Active = models.BooleanField(default = True)
	Parent = models.ForeignKey("self", on_delete = models. CASCADE, null = True, blank = True, related_name = "replies")

	objects = models.Manager


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ["Name", "Content"]
		widgets = {
			"Name": forms.TextInput(attrs={"class": "form-control",
			"placeholder": "Ürününüz için başlık girin"}),
			"Content": forms.TextInput(attrs={"class": "form-control",
			"placeholder": "Ürününüz için başlık girin"}),
						# "category": forms.CheckboxSelectMultiple(attrs={"class":"list-unstyled list- inline"}),
		}
		help_texts = {
			"name": "Başlık girin | Enter title",
			"content": "Ürünü detayla açıklayın | Express your product in detail",
		}
		error_messages = {

		}
		labels = {
			"name": "Başlık",
			"content": "İçerik"
		}
	def clean(self):
		fields = self.cleaned_data
		keys = list(fields.keys())
		print(fields)

	
	def __str__(self):
		return self.name




class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
	
    def __str__(self):
	    return self.choice_text