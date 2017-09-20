from django.shortcuts import render, redirect


# Create your views here.
def index(request):
	if 'single_order_price' not in request.session:	
		request.session['single_order_price'] = 0
	if 'total_price' not in request.session:	
		request.session['total_price'] = 0
	if 'item_count' not in request.session:	
		request.session['item_count'] = 0
		
	context = {}
	return render(request, "main/index.html", context)

def buy(request):
	total_no_of_items_ordered = request.session['item_count']
	total_price = request.session['total_price']
	
	product =  {
		'1': 19.99,
		'2': 29.99,
		'3': 4.99,
		'4': 49.99,
	}
	quantity_ordered = int(request.POST['qty'])
	product_id = request.POST['product_id']
	print "product id****************", product_id
	single_item_price = quantity_ordered * product[product_id]
	request.session['single_order_price'] = single_item_price
	
	total_no_of_items_ordered += quantity_ordered
	request.session['item_count'] = total_no_of_items_ordered
	
	total_price += single_item_price	
	request.session['total_price'] = total_price
	
	return redirect("/checkout")

def checkout(request):
	context = {}
	return render(request, "main/checkout.html", context)