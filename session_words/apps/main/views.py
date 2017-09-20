from django.shortcuts import render, redirect
from datetime import date, datetime
from json import dumps

# Create your views here.
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def index(request):
	if 'saved_session' not in request.session:
		request.session['saved_session'] = []		
	context={}
	return render(request, "main/index.html", context)

def add_word(request):
	if request.POST.get('word') == "":			
		return redirect("/")
		
	if request.POST.get('color') == None:			
		my_color = "black"
	else:		
		my_color = request.POST['color']
	
	if 'big_font' in request.POST:				
		my_font_size = "25"
	else:				
		my_font_size = "8"	
	
	saved_session = {
		'word_to_display': request.POST['word'],
		'color_to_display': my_color,
		'font_size_to_display': my_font_size,
		'time_to_display': dumps(datetime.now(), default=json_serial),
	}
		
	request.session['saved_session'].append(saved_session)
	request.session.modified = True	
	return redirect("/")
	
def clear_session(request):
	request.session['saved_session'] = []
	return redirect("/")
	
	
	