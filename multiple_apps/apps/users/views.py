from django.shortcuts import render, HttpResponse

# Create your views here.
def all_users(request):
	return HttpResponse("placeholder to later display all the list of users")

def register_new_user(request):
	return HttpResponse("placeholder for users to create/register a new user record")
	
def login(request):
	return HttpResponse("placeholder for users to login")