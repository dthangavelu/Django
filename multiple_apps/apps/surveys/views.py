from django.shortcuts import render, HttpResponse

# Create your views here.
def all_surveys(request):
	return HttpResponse("placeholder to display all the surveys created")
	
def create_survey(request):
	return HttpResponse("placeholder for users to add a new survey")