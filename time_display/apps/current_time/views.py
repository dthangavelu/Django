from django.shortcuts import render, redirect, HttpResponse
from time import gmtime, strftime

# Create your views here.
def display_time(request):	 
	context = { 'time': strftime("%b %d, %Y %H:%M %p", gmtime())}
	return render(request, 'current_time/time.html', context )