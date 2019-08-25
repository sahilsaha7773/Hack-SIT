from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from forum import views as fviews
urlpatterns = [
	path('login/', views.user_login, name='login'),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	path('', views.home, name='home'),
	path('register/', views.register, name='register'),
	path('blog/', include('blog.urls', namespace='blog')),
	path('forum/', fviews.post_list, name='list'),
	path('tag/<slug:tag_slug>/',views.home, name='post_list_by_tag'),
]