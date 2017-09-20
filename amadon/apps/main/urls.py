from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^$', index),
	url(r'^buy$', buy),	
	url(r'^checkout$', checkout),		
]
