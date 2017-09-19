from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
def index(request):
	return HttpResponse("</h1>You have landed the Home Page</h1>")
	
def blogs(request):
	return HttpResponse("placeholder to display all the blogs")

def new_blog(request):
	return HttpResponse("placeholder to display a new form to create a new blog")

def create(request):
	return redirect("/")

def blog_number(request, number):	
	return HttpResponse("placeholder to display blog " + number)
	
def edit_blog(request, number):
	return HttpResponse("placeholder to edit blog " + number)
	
def delete_blog(request, number):
	return redirect("/")