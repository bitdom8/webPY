
from django.conf.urls import url
from django.urls import include, path
from .models import *
from .views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

# 	PostListView, 
# 	PostDetailView,
# 	PostCreateView,
# 	PostUpdateView,
# 	PostDeleteView,
# 	UserPostListView,
# 	FileFieldView,
# 	TemplateView
# )


from . import views

urlpatterns = [
	path('', PostListView.as_view(), name ="blog-home"),
	path('user/<str:username>', UserPostListView.as_view(), name ="user-posts"),
	path('post/<int:pk>/', PostDetailView.as_view(), name ="post-detail"),

	path('post/new/', PostCreateView.as_view(model=Post, success_url=('/')), name ="post-create"),
	# path('post/new/', PostCreateView.as_view(), name ="post-create"),
	path('simple_upload/', views.simple_upload, name ="simple_upload"),
	path('post/<int:pk>/delete/', PostDeleteView.as_view(), name ="post-delete"),
	path('about/', views.about, name ="blog-about"),
	path('game/', views.game, name ="blog-game"),
	path('contact/', views.contact, name ="blog-contact"),

	url(r'^$', views.HomeView.as_view(), name='home'),
	path('upload/', FileFieldView.as_view(), name ="File-Field"),
	path('index/', views.index, name ="blog-index"),
	path('post/<int:pk>/update/', PostUpdateView.as_view(), name ="post-update"),
	#path('post/<int:pk>/update/', index3.as_view(), name ="index3")

]


