from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^$', all_users),
	url(r'^new$', register_new_user),
	url(r'^register$', register_new_user),
	url(r'^login$', login),
	
]