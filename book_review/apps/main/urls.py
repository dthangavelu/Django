from django.conf.urls import url
from .views import *

urlpatterns = [	
	url(r'^$', index),	
	url(r'^login/$', login),
	url(r'^register/$', register_user),
	url(r'^logout/$', logout),
	url(r'^books/$', main_pg),
	url(r'^books/add/$', display_add_book_and_review_pg),
	url(r'^books/add_book_review/$', add_book_and_review),	
	url(r'^books/(?P<id>\d+)/$', review_a_book),	
	url(r'^books/details/(?P<id>\d+)/$', book_details_pg),	
	url(r'^users/(?P<id>\d+)/$', user_details_pg),	
]



