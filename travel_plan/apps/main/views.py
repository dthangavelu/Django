from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from datetime import datetime
import bcrypt, re
from django.db import connection
import sqlite3

# Create your views here.

def isValidName(name):
	if len(name) < 3:
		return "must be 3 or more characters long"
	#if re.match('^[a-zA-Z]+$', name) == None:
	#	return "only alphabets allowed"
	return True
	
def isValidPwdLen(pwd):
	if len(pwd) < 8:
		return "Password must be of minimum 8 characters long"
	return True
			
def isPwdMatchesConfirmPwd(pwd, cPwd):
	if pwd != cPwd:
		return "Passwords do not match"
	return True
	

def index(request):
	if 'logged_in_user' not in request.session:
		request.session['logged_in_user'] = ""
			
	context={}	
	return render(request, "main/index.html", context)

def login(request):	
	context = {}
	err_msg = ""
	
	form_username = request.POST['username']	
	form_pwd = request.POST['password']	
	
	if (form_username == ""):
		err_msg += "User name cannot be empty\n\n"
	
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
	
	users = User.objects.filter(username = form_username)	
	request.session['logged_in_user'] = users[0].username
	
	return redirect("/travels/main_dashboard")
	
def register_user(request):
	context = {}
	err_msg = ""
	form_name = request.POST['name']		
	form_username = request.POST['username']		
	form_pwd = request.POST['password']
	form_confirm_pwd = request.POST['confirm_password']
	
	if(form_name == ""):		
		err_msg += "Name cannot be empty\n\n"	
	elif isValidName(form_name) != True:
		err_msg += "Name " + isValidName(form_name) + "\n\n"
				
	if(form_username == ""):		
		err_msg += "Username cannot be empty\n\n"		
	elif isValidName(form_username) != True:
		err_msg += "Username " + isValidName(form_username) + "\n\n"
			
	if (form_pwd == ""):
		err_msg += "Password cannot be empty\n\n"	
	elif isValidPwdLen(form_pwd) != True:
		err_msg += isValidPwdLen(form_pwd) + "\n\n"	
	elif isPwdMatchesConfirmPwd(form_pwd, form_confirm_pwd) != True:
		err_msg += isPwdMatchesConfirmPwd(form_pwd, form_confirm_pwd) + "\n\n"
	
	users = User.objects.filter(username = form_username)
	
	if users:
		err_msg += "Username already exists in system. Please register with different username"
	
	if len(err_msg) > 0:		
		messages.error(request, err_msg, "")
		return redirect("/")
		
	request.session['logged_in_user'] = form_username	
	form_name = form_name.strip().lower()	
	form_username = form_username.strip()	
	hash_pwd = bcrypt.hashpw(form_pwd.encode(), bcrypt.gensalt())
	User.objects.create(name=form_name, username=form_username, password=hash_pwd, created_at=datetime.now())
		
	return redirect("/travels/main_dashboard")
		
def logout(request):
	request.session['logged_in_user'] = ""		
	return redirect("/")
	
	
def display_add_trip_pg(request):	
	context = {}
	return render(request, "main/add_trip.html", context)

def add_trip(request):
	err_msg = ""
	form_dest = request.POST['destination']
	form_desc = request.POST['desc']
	form_start_date = request.POST['start_date']
	form_end_date = request.POST['end_date']

	if form_end_date < form_start_date:
		err_msg += "End date can't precede start date"
	
	if len(err_msg) > 0:
		messages.error(request, err_msg, "")
		return redirect("/travels/add")
		
	users = User.objects.filter(username = request.session['logged_in_user'])	
	#print "userid*****************", users[0].id
	travel = TravelPlan.objects.create(destination=form_dest, description=form_desc, travel_start_date=form_start_date, travel_end_date=form_end_date, created_at=datetime.now(), travel_panned_by=users[0])
	
	cursor = connection.cursor()
	cursor.execute("INSERT INTO main_travelplan_joined_users (travelplan_id, user_id) VALUES ({id}, {user_id})".\
        format(id=travel.id, user_id=users[0].id))
	context = {}
	
	return redirect("/travels/main_dashboard")

def main_dashboard(request):	
	users = User.objects.filter(username = request.session['logged_in_user'])
	user_id =  users[0].id
	
	cursor = connection.cursor()
	cursor.execute("select main_user.name, main_travelplan.destination, main_travelplan.travel_start_date, main_travelplan.travel_end_date, main_travelplan.description, main_travelplan.id, main_travelplan.travel_panned_by_id from main_travelplan join main_user on main_user.id = main_travelplan.travel_panned_by_id where main_travelplan.travel_panned_by_id not in ({id})".format(id=user_id))
	all_travel_plans = cursor.fetchall()
	
	cursor = connection.cursor()
	
	#cursor.execute('''select destination, travel_start_date, travel_end_date, description, id, travel_panned_by_id from main_travelplan where travel_panned_by_id = ''' + str(user_id))
	cursor.execute('''select main_travelplan.destination, main_travelplan.travel_start_date, main_travelplan.travel_end_date, main_travelplan.description from main_travelplan_joined_users join main_travelplan on main_travelplan.id=main_travelplan_joined_users.travelplan_id where main_travelplan_joined_users.user_id=''' + str(user_id))
	
	user_travel_plan = cursor.fetchall()
			
	context ={
		'all_travel_plans': all_travel_plans,
		'user_travel_plan': user_travel_plan,
	}
	return render(request, "main/travels.html", context)
	
def join_travel(request, id):
	users = User.objects.filter(username = request.session['logged_in_user'])
	user_id =  users[0].id
	
	cursor = connection.cursor()
	cursor.execute("INSERT INTO main_travelplan_joined_users (travelplan_id, user_id) VALUES ({id}, {user_id})".\
        format(id=id, user_id=user_id))
	joined_travel_plan = cursor.fetchall()	

	return redirect("/travels/main_dashboard")
	
def display_destinations_detail_pg(request, id):
	cursor = connection.cursor()
	cursor.execute('''select main_travelplan.destination, main_user.name, main_travelplan.description, main_travelplan.travel_start_date, main_travelplan.travel_end_date from main_travelplan join main_user on main_user.id=main_travelplan.travel_panned_by_id where main_travelplan.id = ''' + str(id))
	travel_details = cursor.fetchone()	
	
	context = {
		'destination': travel_details[0],
		'planned_by': travel_details[1],
		'description': travel_details[2],
		'start': travel_details[3],
		'end': travel_details[4],
	}
	return render(request, "main/destinations_detail.html", context)
	


	
	