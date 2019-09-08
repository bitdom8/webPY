from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.template import loader

from django.views.generic import (
	ListView,
	DetailView, 
	CreateView,
	UpdateView,
	DeleteView,
	FormView
)

class HomeView(DetailView, FormView, CreateView):
	template_name = 'blog/home.html'
	data2 = Gallery.objects.all()


	def index(self, request, *args, **kwargs):
		form = PostForm()
		data = Post.objects.all()
		data2 = Gallery.objects.all()
		comment_form = CommentForm(request.POST, request.FILES)

		

		if request.method == 'POST':
			form = PostForm(request.POST, request.FILES)
			comment_form = CommentForm(request.POST, request.FILES)
			files = request.FILES.getlist("image")
			

			if form.is_valid():
				post = form.save(commit = False)
				post.save()
				for f in files:			
					gallery = Gallery(post=post, image = f)
					gallery.save()
				return render(request, 'blog/home.html', {"title": "add new", "comment_form": comment_form,  'form': form, "data": data, "files1": files, "data2":data2})
		return render(request, 'blog/home.html', {"title": "add new", "comment_form": comment_form,"data": data, "data2":data2, 'form': form, })







def contact(request):

	if(request.method == "GET" and request.GET.get("method") == "delete" and request.GET.get("id")):
		rec = Contact.objects.filter(id=request.GET.get("id"))
		rec.delete()

	if(request.method == "GET" and request.GET.get("method") == "edit" and request.GET.get("id")):
		cnt = Contact.objects.filter(id=request.GET.get("id")).get()
		return render(request, "blog/edit.html", {"title":"Contact Page Title", "row" : cnt})

	if(request.method == "POST"):
		# data = Contact(request.POST)
		if(request.GET.get("method") == "edit"):
			rec = Contact.objects.filter(id=request.GET.get("id"))
			rec.update(
				name = request.POST["name"],
				email = request.POST["email"],
				address = request.POST["address"],
				city = request.POST["city"],
			)
			return HttpResponseRedirect("/contact")

		else:
			data = Contact(
			name = request.POST["name"],
			email = request.POST["email"],
			address = request.POST["address"],
			city = request.POST["city"],
			)
			data.save()
	cnt = Contact.objects.all()
	return render(request, "blog/contact.html", {"title":"Contact PageRows", "rows": cnt})
	#  "email": email, "address":address, "city": city, "zipcode": zipcode}) 

	# return render(request, "blog/contact.html", {"title": "Contact Page Title"})

# no more relevant below "posts"
# posts = [
# 	{

# 		"author": "CoreyMS",
# 		"title": "Blog Post ",
# 		"content": "First post content",
# 		"date_posted": "August 27, 2018",
# 	}
# ]
# APP
#def index(request):
  #  return render(request, "app/videoplay.html", {'media': MEDIA_ROOT})

# def home(request):

# 	form = PostForm
# 	post = Post
# 	context = {
# 		"posts" : Post.objects.all(),
# 		"comments": Comment.objects.all(),
# 		"gallerys": Gallery.objects.all(),
# 		'post': post,
# 		'form': form,
# 		"comment":comment,

# 	}
# 	return render(request, "blog/home.html", context)

class PostListView(ListView):
	model = Post
	template_name = "blog/home.html"       # <app>/model>_viewtype>html
	context_object_name = "posts"
	ordering = ["-date_posted"]
	paginate_by = 15

	template = loader.get_template('blog/index.html')

	def get_absolute_url(self):
		return reverse("post-detail", kwargs={"pk": self.pk})

	def post_detail(self, request, data, slug=None):
		post = get_object_or_404(Post, slug=slug)
		data = Post.objects.all()
		today = timezone.now().date()
		return render(self.request, "blog/post_detail.html", {'post': post, "data":data, "today": today, "form": form})

class UserPostListView(ListView):
	model = Post
	template_name = "blog/user_posts.html"       # <app>/model>_viewtype>html
	context_object_name = "posts"
	paginate_by = 15

	def get_absolute_url(self):
		return reverse("post-detail", kwargs={"pk": self.pk})

	def get_queryset(self):
		user = get_object_or_404(User, username = self.kwargs.get("username"))
		return Post.objects.filter(author = user).order_by("-date_posted")
		
class PostDetailView(DetailView, FormView):
	model = Post
	form_class = PostForm
	data = Post.objects.all()
	data2 = Gallery.objects.all()
	context = {"data": data, "data2" : data2}


	def post_detail(self, request, data, slug=None):
		post = get_object_or_404(Post, slug=slug)
		data = Post.objects.all()
		today = timezone.now().date()
		return render(self.request, "blog/post_detail.html", {'post': post, "data":data, "today": today, "form": form})


	# def post(self, request, *args, **kwargs):
	# 	form = PostForm()
	# 	data = Post.objects.all()		

	# 	if request.method == 'POST':
	# 		form = PostForm(request.POST, request.FILES)
	# 		files = request.FILES.getlist("image")
			
	# 		if form.is_valid():
	# 			post = form.save(commit = False)
	# 			post.save()
	# 			data2 = Gallery.objects.all()
					
	# 			for f in files:
					
	# 				# post = Post(thumbnail= f)
	# 				gallery = Gallery(post = post, image = f)
	# 				gallery.save()
	# 				messages.success(request, f"Photos uploaded" + gallery.image.url)
	# 			data2 = Gallery.objects.all()
					

	# 			return redirect('/', {"title": "add one"})
				

	# 	return render(self.request, 'blog/home.html', {"title": "add one", "form": form, "data": data, "data2": data2})

	
class PostCreateView(FormView, LoginRequiredMixin, CreateView):
	form_class = PostForm
	model = Post
	
	# category = Category.objects.all()
	def get_absolute_url(self):
		return reverse("post-detail", kwargs={"pk": self.pk})

	def post(self, request, *args, **kwargs):
		form = PostForm()
		data = Post.objects.all()
		data2 = Gallery.objects.all()
		

		if request.method == 'POST':
			form = PostForm(request.POST, request.FILES)
			files = request.FILES.getlist("image")
			
			if form.is_valid():
				post = form.save(commit = False)
				post.save()
				data2 = Gallery.objects.all()
					
				for f in files:
					
					# post = Post(thumbnail= f)
					gallery = Gallery(post = post, image = f)
					gallery.save()
					messages.success(request, f"Photos uploaded" + gallery.image.url)
				data2 = Gallery.objects.all()
					

				return redirect('/', {"title": "add one"})
				

		return render(self.request, 'blog/home.html', {"title": "add one", "form": form, "data": data, "data2": data2})


class FileFieldView(FormView):
	form_class = FileFieldForm
	template_name = 'blog/upload.html'  # Replace with your template.
	success_url = '/'  # Replace with your URL or reverse().


# 	def post(self, request, *args, **kwargs):
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         files = request.FILES.getlist('file_field')
#         if form.is_valid():
#             for f in files:
#                 ...  # Do something with each file.
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)



@login_required
def index(request, *args, **kwargs):
	form = PostForm()
	data = Post.objects.all()
	data2 = Gallery.objects.all()
	comment_form = CommentForm(request.POST, request.FILES)

	

	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES)
		comment_form = CommentForm(request.POST, request.FILES)
		files = request.FILES.getlist("image")
		

		if form.is_valid():
			post = form.save(commit = False)
			post.save()


			for f in files:
				
				gallery = Gallery(post=post, image = f)
				gallery.save()

				# uplo = FileSystemStorage().url(FileSystemStorage().save(request.FILES['image'].name, request.FILES['image']))
				# image.save(request.image.path)

				

				# myfile = request.FILES['myfile']
				# fs = FileSystemStorage()
				# filename = fs.save(myfile.name, myfile)
				# uploaded_file_url = fs.url(filename)
			
			return render(request, 'blog/index.html', {"title": "add new", "comment_form": comment_form,  'form': form, "data": data, "files1": files, "data2":data2})
	return render(request, 'blog/index.html', {"title": "add new", "comment_form": comment_form,"data": data, "data2":data2, 'form': form, })




def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'blog/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'blog/simple_upload.html', {"title" : "Simple_Upload"})




class PostUpdateView(FormView, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	form_class = PostForm
	model = Post


	
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False




# class index3(FormView):
# 	template_name = "blog/index.html"
# 	form_class = CommentForm
# 	success_url = "blog/index.html"



class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = "/"

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


def game(request):
	return render(request, "blog/game.html", {"title" : "Game"})

def about(request):
	return render(request, "blog/about.html", {"title" : "About"})







def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)



def index2(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)
