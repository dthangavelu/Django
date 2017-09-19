from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^$', get_rand_word),
	url(r'^random_word$', get_rand_word),	
	url(r'^random_word/reset/$', reset),	
]
