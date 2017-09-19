from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^blogs/$', views.blogs),
	url(r'^blogs/new/', views.new_blog),
	url(r'^blogs/create/', views.create),
	url(r'^blogs/(?P<number>\d+)$', views.blog_number),	
	url(r'^blogs/(?P<number>\d+)/edit$', views.edit_blog),	
	url(r'^blogs/(?P<number>\d+)/delete$', views.delete_blog),
]