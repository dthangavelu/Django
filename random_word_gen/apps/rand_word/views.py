from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string

# Create your views here.
def get_rand_word(request):	
	myRandomString = get_random_string(length=14)
	count = request.session['attempt_counter']
	request.session['attempt_counter'] =  count + 1
	print "attempt*****************", request.session['attempt_counter'] 
	context = {		
		'word': myRandomString,		
	}	
	return render(request, "rand_word/rand_word_gen.html", context)

def reset(request):	
	request.session['attempt_counter'] = 0
	print "attempt in RESET*****************", request.session['attempt_counter'] 
	return redirect("/")