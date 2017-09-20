from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^$', index),
	url(r'^add_word$', add_word),	
	url(r'^clear_session$', clear_session),		
]
