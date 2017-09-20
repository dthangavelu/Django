from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^$', index),
	url(r'^results$', results),	
	#url(r'^random_word/reset/$', reset),	
]
