from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
app_name = "forum"
urlpatterns = [
	path('create/', views.question_create, name='create'),
	path('detail/<int:id>/<slug:slug>/', views.question_detail, name='detail'),
	# path('delete/<int:id>/<slug:slug>/', views.report_delete, name='delete'),
	# path('deleted/', views.delete_done, name='delete_done'),
	path('like/', views.post_like, name='like'),
	path('account/', include('account.urls')),
	path('', views.post_list, name='list'),
	path('ratings/', include('star_ratings.urls', namespace='ratings'), name='ratings'),

]