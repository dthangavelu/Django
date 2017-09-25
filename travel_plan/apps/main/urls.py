from django.conf.urls import url
from .views import *

urlpatterns = [	
	url(r'^$', index),	
	url(r'^login/$', login),
	url(r'^register/$', register_user),
	url(r'^logout/$', logout),
	url(r'^travels/add$', display_add_trip_pg),	
	url(r'^travels/add_trip$', add_trip),	
	url(r'^travels/main_dashboard$', main_dashboard),
	url(r'^travels/(?P<id>\d+)/$', join_travel),
	url(r'^travels/details/(?P<id>\d+)/$', display_destinations_detail_pg),

	# url(r'^users/$', index),
	# url(r'^users/new$', display_new_user_page),	
	# url(r'^users/create$', create_new_user_db),	
	# url(r'^users/(?P<id>\d+)/$', display_user_by_id),	
	# url(r'^users/(?P<id>\d+)/destroy$', delete_user_by_id),	
	# url(r'^users/(?P<id>\d+)/edit$', display_edit_user_by_id_page),	
]



