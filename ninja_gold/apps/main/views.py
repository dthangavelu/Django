from django.shortcuts import render, redirect
from random import randint
import datetime

# Create your views here.
def index(request):
	if 'saved_session' not in request.session:
		request.session['saved_session'] = []		
		
	if "total_gold_earned" not in request.session:
		request.session['total_gold_earned'] = 0
		
	context = {}
	return render(request, "main/index.html", context)

def process_money(request):	
	total_gold_earned = request.session['total_gold_earned'] 
	
	fmt = '%Y-%m-%d %H:%M:%S %Z'
	d = datetime.datetime.now()
	d_string = d.strftime(fmt)	
	
	building_choice = request.POST['building']	
	
	rand_gold = {
		'farm': (randint(10, 20)),
		'cave': (randint(5, 10)),
		'house': (randint(2, 5)),
		'casino': (randint(-50, 50)),
	}
	
	gold_earned = rand_gold[building_choice]
	total_gold_earned += gold_earned
	request.session['total_gold_earned'] = total_gold_earned
	
	if building_choice != "casino":
		my_color = "green"
		text_to_display = "Earned " + str(gold_earned) + " golds from " + building_choice + " (" + d_string + ")"
	elif gold_earned < 0:
		my_color = "red"
		text_to_display = "Entered a casino and lost " + str(abs(gold_earned)) + " golds... Ouch... (" + d_string + ")"
	else: 
		my_color = "green"
		text_to_display = "Entered a casino and earned " + str(gold_earned) + " golds... WOW!... (" + d_string + ")"

	result = {
		'color': my_color,
		'text_to_display': text_to_display,		
	}
	
	request.session['saved_session'].append(result)
	request.session.modified = True	
	return redirect("/")