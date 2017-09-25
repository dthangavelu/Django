from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from .models import *
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
		 
	if 'user_email' not in request.session:
		request.session['user_email'] = ""
		
	context={}	
	return render(request, "main/index.html", context)

def login(request):		
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
	request.session['user_email'] = users[0].email
	
	cursor = connection.cursor()
	cursor.execute('''select main_review.content, main_review.rating, main_review.updated_at, main_book.title, main_user.first_name, main_book.id, main_user.id as user_id from main_review join main_book on main_review.reviewed_books_id = main_book.id join main_user on main_user.id = main_review.reviewer_id  order by main_review.updated_at desc limit 3''')
	recent_reviews = cursor.fetchall()
	cursor.execute('''select distinct(main_book.title), main_book.id from main_review join main_book where main_review.reviewed_books_id = main_book.id order by main_review.updated_at desc''')	
	all_reviews = cursor.fetchall()
	
	context = {
		'all_reviews': all_reviews,
		'recent_reviews': recent_reviews
	}
	return render(request, "main/home_main.html", context)
	
def register_user(request):
	context = {}
	err_msg = ""
	form_fn = request.POST['first_name']
	form_ln = request.POST['last_name']
	form_email = request.POST['email']	
	form_email = form_email.lower()
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
	request.session['user_email'] = form_email
	
	hash_pwd = bcrypt.hashpw(form_pwd.encode(), bcrypt.gensalt())
	User.objects.create(first_name=form_fn, last_name=form_ln, email=form_email, password=hash_pwd, created_at=datetime.now())
		
	cursor = connection.cursor()
	cursor.execute('''select main_review.content, main_review.rating, main_review.updated_at, main_book.title, main_user.first_name, main_book.id, main_user.id as user_id from main_review join main_book on main_review.reviewed_books_id = main_book.id join main_user on main_user.id = main_review.reviewer_id  order by main_review.updated_at desc limit 3''')
	recent_reviews = cursor.fetchall()
	cursor.execute('''select distinct(main_book.title), main_book.id from main_review join main_book where main_review.reviewed_books_id = main_book.id order by main_review.updated_at desc''')	
	all_reviews = cursor.fetchall()
	
	context = {
		'all_reviews': all_reviews,
		'recent_reviews': recent_reviews
	}	
		
	return render(request, "main/home_main.html", context)	
	
def logout(request):
	request.session['logged_in_user'] = ""	
	request.session['is_register_or_login'] = ""
	request.session['user_email'] = ""
	return redirect("/")
	
def display_add_book_and_review_pg(request)	:
	authors = Author.objects.all()
	context = {
		'authors': authors,
	}
	return render(request, "main/add_book_and_review_pg.html", context)
	
def main_pg(request):
	cursor = connection.cursor()
	cursor.execute('''select main_review.content, main_review.rating, main_review.updated_at, main_book.title, main_user.first_name, main_book.id, main_user.id as user_id from main_review join main_book on main_review.reviewed_books_id = main_book.id join main_user on main_user.id = main_review.reviewer_id  order by main_review.updated_at desc limit 3''')
	recent_reviews = cursor.fetchall()
	cursor.execute('''select distinct(main_book.title), main_book.id, main_user.id as user_id from main_review join main_book on main_review.reviewed_books_id = main_book.id join main_user on main_user.id = main_review.reviewer_id  order by main_review.updated_at desc''')
	all_reviews = cursor.fetchall()
	
	context = {
		'all_reviews': all_reviews,
		'recent_reviews': recent_reviews
	}			
	return render(request, "main/home_main.html", context)
	
def add_book_and_review(request):
	title = request.POST['bk_title']
	title = title.strip().lower()
	
	author_list = request.POST['author_list']
	input_author = request.POST['author']
	
	review = request.POST['review']
	review = review.strip()
	
	rating = request.POST['rating']
		
	if author_list != "default":
		author = author_list
	else:
		author = input_author
		author = author.strip().lower()
		
	if not Author.objects.filter(name = author):		
		author_db = Author.objects.create(name=author)
	
	book = Book.objects.filter(title=title)
	user_id = User.objects.filter(email=request.session['user_email'])[0].id
	
	if not book:
		book = Book.objects.create(title=title, author_id=Author.objects.filter(name = author)[0].id)
		book_id = book.id
	else:
		book_id = book[0].id
		
	Review.objects.create(content=review, rating=rating, updated_at=datetime.now(), reviewed_books_id= book_id, reviewer_id=user_id)
		
	cursor = connection.cursor()		
	cursor.execute('''select main_review.content, main_review.rating, main_review.updated_at, main_book.title, main_author.name, main_user.first_name, main_book.id, main_user.id from main_review join main_book on main_book.id = main_review.reviewed_books_id join main_user on main_review.reviewer_id = main_user.id join main_author on main_author.id = main_book.author_id where reviewed_books_id=''' + str(book_id))		
	book_reviews = cursor.fetchall()
	print "user id********************", book_reviews
	context = {		
		'book_id': book_id,		
		'book_title': book_reviews[0][3],
		'book_author': book_reviews[0][4],
		'book_reviews': book_reviews,
	}
	return render(request, "main/add_review_for_a_book.html", context)
	
def book_details_pg(request, id):
	book = Book.objects.filter(id=id)
	
	cursor = connection.cursor()	
	cursor.execute('''select main_review.content, main_review.rating, main_review.updated_at, main_book.title, main_author.name, main_user.first_name, main_book.id, main_user.id from main_review join main_book on main_book.id = main_review.reviewed_books_id join main_user on main_review.reviewer_id = main_user.id join main_author on main_author.id = main_book.author_id where reviewed_books_id=''' + str(id))		
	book_reviews = cursor.fetchall()
		
	context = {
		'book_id': book[0].id,
		'book_title': book_reviews[0][3],
		'book_author': book_reviews[0][4],
		'book_reviews': book_reviews,
	}
	return render(request, "main/add_review_for_a_book.html", context)

def user_details_pg(request, id):	
	cursor = connection.cursor()
	cursor.execute('''select count(*) from main_review where main_review.reviewer_id=''' + str(id))
	review_count = cursor.fetchall()
	cursor.execute('''select distinct(main_book.title), main_book.id from main_review join main_book on main_book.id = main_review.reviewed_books_id where main_review.reviewer_id=''' + str(id))
	reviewed_books = cursor.fetchall()
	cursor.execute('''select main_user.first_name, main_user.email from main_user where main_user.id=''' + str(id))
	user_data = cursor.fetchall()
		
	context = {
		'user_data': user_data,
		'review_count': review_count,
		'reviewed_books': reviewed_books,
	}
	return render(request, "main/user_details_pg.html", context)
	
def review_a_book(request, id):	
	review = request.POST['review']
	rating = request.POST['rating']
	
	user_id = User.objects.filter(email=request.session['user_email'])[0].id
	
	Review.objects.create(content=review, rating=rating, updated_at=datetime.now(), reviewed_books_id= id, reviewer_id=user_id)
		
	cursor = connection.cursor()	
	cursor.execute('''select main_review.content, main_review.rating, main_review.updated_at, main_book.title, main_author.name, main_user.first_name from main_review join main_book on main_book.id = main_review.reviewed_books_id join main_user on main_review.reviewer_id = main_user.id join main_author on main_author.id = main_book.author_id where reviewed_books_id=''' + str(id))		
	book_reviews = cursor.fetchall()
	
	context = {
		'book_title': book_reviews[0][3],
		'book_author': book_reviews[0][4],
		'book_reviews': book_reviews,
	}
	
	return render(request, "main/add_review_for_a_book.html", context)

