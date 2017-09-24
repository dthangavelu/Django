from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from datetime import datetime
import bcrypt, re

# Create your views here.

def isValidEmail(email):
	if len(email) < 7 or re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email) == None:
		return "Email should be of valid format. Format example@example.xxx."
	return True	

def isValidName(name):
	if len(name) < 2:
		return "must be 2 or more characters long"
	if re.match('^[a-zA-Z]+$', name) == None:
		return "only alphabets allowed"
	return True
	
def isValidPwdLen(pwd):
	if len(pwd) < 8:
		return "Password must be of minimum 8 characters long"
	return True
	return False	
		
def isPwdMatchesConfirmPwd(pwd, cPwd):
	if pwd != cPwd:
		return "Passwords do not match"
	return True
	

def index(request):
	if 'logged_in_user' not in request.session:
		request.session['logged_in_user'] = ""
	
	if 'is_register_or_login' not in request.session:
		request.session['is_register_or_login'] = ""
		
	context={}	
	return render(request, "main/index.html", context)

def login(request):
	print "in login in view**********************", request.method
	context = {}
	err_msg = ""
	form_email = request.POST['email']	
	form_pwd = request.POST['password']	
		
	if (form_email == ""):
		err_msg += "Email cannot be empty\n\n"	
	elif isValidEmail(form_email) != True:
		err_msg += isValidEmail(form_email) + " \n\n"
		
	if (form_pwd == ""):
		err_msg += "Password cannot be empty\n\n"	
		
	if len(err_msg) > 0:		
		messages.error(request, err_msg, "")
		return redirect("/")
	
	err_msg = User.objects.login_validator(request.POST)
	if len(err_msg) > 0:	
		for tag, error in err_msg.iteritems():
			messages.error(request, error, "")
		return redirect("/")
	
	users = User.objects.filter(email = form_email)	
	request.session['logged_in_user'] = users[0].first_name
	request.session['is_register_or_login'] = "logged in!"	
	
	return render(request, "main/success.html", context)
	
def register_user(request):
	context = {}
	err_msg = ""
	form_fn = request.POST['first_name']
	form_ln = request.POST['last_name']
	form_email = request.POST['email']	
	form_pwd = request.POST['password']
	form_confirm_pwd = request.POST['confirm_password']
	
	if(form_fn == ""):		
		err_msg += "First Name cannot be empty\n\n"	
	elif isValidName(form_fn) != True:
		err_msg += "First Name " + isValidName(form_fn) + "\n\n"
				
	if(form_ln == ""):		
		err_msg += "Last Name cannot be empty\n\n"		
	elif isValidName(form_ln) != True:
		err_msg += "Last Name " + isValidName(form_ln) + "\n\n"
		
	if (form_email == ""):
		err_msg += "Email cannot be empty\n\n"	
	elif isValidEmail(form_email) != True:
		err_msg += isValidEmail(form_email) + " \n\n"
	
	if (form_pwd == ""):
		err_msg += "Password cannot be empty\n\n"	
	elif isValidPwdLen(form_pwd) != True:
		err_msg += isValidPwdLen(form_pwd) + "\n\n"	
	elif isPwdMatchesConfirmPwd(form_pwd, form_confirm_pwd) != True:
		err_msg += isPwdMatchesConfirmPwd(form_pwd, form_confirm_pwd) + "\n\n"
		
	if len(err_msg) > 0:		
		messages.error(request, err_msg, "")
		return redirect("/")
		
	request.session['logged_in_user'] = form_fn	
	request.session['is_register_or_login'] = "registered!"
		
	hash_pwd = bcrypt.hashpw(form_pwd.encode(), bcrypt.gensalt())
	User.objects.create(first_name=form_fn, last_name=form_ln, email=form_email, password=hash_pwd, created_at=datetime.now())
		
	return render(request, "main/success.html", context)
	
	
def logout(request):
	request.session['logged_in_user'] = ""	
	request.session['is_register_or_login'] = ""
	return redirect("/")
	
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


