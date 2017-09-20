from django.shortcuts import render

# Create your views here.
def index(request):
	if 'count' in request.session:
		counter = request.session['count']	
		request.session['count'] = counter + 1
	else:
		request.session['count'] = 1
		
	context = {}
	return render(request, "my_survey/index.html", context)

def results(request):	
	context = {
		'name': request.POST['user_name'],
		'fav_lang': request.POST['fav_lang'],
		'location': request.POST['location'],
		'comment': request.POST['comment'],
	}
	return render(request, "my_survey/results.html", context)