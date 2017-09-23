from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

# Create your views here.
def index(request):
	context={
		'all_users': User.objects.all()
	}	
	return render(request, "main/index.html", context)

def display_new_user_page(request):
	context={}
	return render(request, "main/add_new_user.html", context)

def create_new_user_db(request):
	fn = request.POST['first_name']
	ln = request.POST['last_name']
	form_email = request.POST['email']
	err = ""
	#print "fn: {} | ln: {} | email: {}".format(fn, ln, form_email)
	
	if(fn == ""):		
		err += "First Name cannot be empty\n"
				
	if(ln == ""):		
		err += "Last Name cannot be empty\n"		
		
	if(form_email == ""):		
		err += "Email cannot be empty\n"		
	
	if len(err) > 0:		
		messages.error(request, err, "")
		return render(request, "main/add_new_user.html", {})
	
	User.objects.create(first_name=fn, last_name=ln, email=form_email)
	return redirect("/users")
	
	
def display_user_by_id(request, id):
	print "request.method*******************", request.method
	user = User.objects.get(id=id)		
	
	context = {
		'user': user,
	}
		
	if request.method == "POST":
		fn = request.POST['first_name']
		ln = request.POST['last_name']
		form_email = request.POST['email']
		err = ""
		#print "fn: {} | ln: {} | email: {}".format(fn, ln, form_email)
		
		if(fn == ""):		
			err += "First Name cannot be empty\n"
					
		if(ln == ""):		
			err += "Last Name cannot be empty\n"		
			
		if(form_email == ""):		
			err += "Email cannot be empty\n"		
		
		if len(err) > 0:		
			messages.error(request, err, "")
			return render(request, "main/edit_user.html", context)
		else:
			user.first_name = fn
			user.last_name = ln
			user.email = form_email
			user.save()
	return render(request, "main/show_user.html", context)
	
def delete_user_by_id(request, id):
	user = User.objects.get(id=id)
	user.delete()
	return redirect("/users")

def display_edit_user_by_id_page(request, id):
	user = User.objects.get(id=id)		
	context = {
		'user': user,
	}
	return render(request, "main/edit_user.html", context)


