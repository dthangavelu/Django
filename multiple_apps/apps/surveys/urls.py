from django.conf.urls import url
#from . import views
from .views import *

urlpatterns = [
	url(r'^$', all_surveys),
	url(r'^new$', create_survey),
]