from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from items.models import Items, Order
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from django.core import serializers
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# ITEMS METHOD DISPLAYS THE LIST OF ITEMS FOR SALE
@login_required(login_url = login)
def items(request):
	#generate a list of all the items 
	items_list = Items.objects.all()

	#GET request, search for items  
	if request.GET.get('search'):
		items_list = Items.objects.filter(name__contains=request.GET.get('search'))

	# nest within the ability to search within price ranges
	if request.GET.get('price') == "1":
		items_list = items_list.filter(price__lte=25)
	if request.GET.get('price') == "2":
		items_list = items_list.filter(price__gte=25, price__lte=200)
	if request.GET.get('price') == "3":
		items_list = items_list.filter(price__gte=200)

	#Use the Django Built in paginator to display 4 items per page
	paginator = Paginator(items_list, 4)

	#Implement exceptions to prevent crashing
	page = request.GET.get('page')
	try:
		items = paginator.page(page)
		'''What does PageNotAnInteger do?'''
	except PageNotAnInteger: 
		items = paginator.page(1)
	except Emptypage:
		items = paginator.page(paginator.num)

	#converting request into Json format
	#Query Param, if the request ID is format, check that the value is json
	if request.GET.get('format') == 'json':
		data = serializers.serialize("json", items) #convert the items into json format
		return HttpResponse(data, content_type='application/json')#return the data in json format
	else:
		return render(request, 'items/items.html', {"items": items}) #otherwise redner and pass in items to html


# SHOW METHOD DISPLAYS ONE ITEM
@login_required(login_url = login)
def show(request, item_id):
	# Obtain a status to check if there is an item object, if there is a item in the list status = 1
	status = int(len(Items.objects.filter(id = item_id)))

	#Use exception to check if an item exists
	try:
		item = Items.objects.get(pk=item_id)
	except Items.DoesNotExist:
		return HttpResponse("ITEM DOES NOT EXIST")

	#render and pass in the item, item id, and the status to the html file to display
	return render(request, 'items/show.html', {'item': item, 'item_id': item_id, 'status': status})

def total_price(item_list):
	price = 0
	for item in item_list:
		item.order_status = 2
		price = price + item.price
	return price




# CART METHOD CHECKS A USER'S ORDER AND DISPLAYS THE ITEMS IN THEIR CART
@login_required(login_url = login)
def cart(request, item_id):

	# verify user by authenticating
	if not request.user.is_authenticated():
		return HttpResponse("CANNOT ACCESS PAGE")

	#check to see if the user has an order with an order_status = 1 (in shopping cart)
	o = Order.objects.filter(user=request.user, order_status = 1)

	if o: # if there is an order for that user (o == True), this statement will proceed to add item
		o[0].user = request.user #assign user to order
		o[0].save() #save 
		o[0].items.add(Items.objects.get(pk=item_id)) #add item to the oder
		o[0].save() #save the order
		item_list = o[0].items.all() #generate a list of items to pass into html file
		# print "item list: \n", o[0].items.all() #TESTING IN RPEL

		#Calculate the total price
		price = 0
		for items in item_list:
			price = price + items.price
		print "\nin cart: ", price , "\n"
		#render and pass in the data to html file and display
		return render(request, 'items/cart.html', {'item_list':item_list, 'price' : price})
		
	else:
		# if the user does not have an order, create an order  
		o = Order()
		o.order_status = 1 #change order_status to 1,
		o.user = request.user
		o.save()
		o.items.add(Items.objects.get(pk=item_id)) #add item to order
		o.save() #dont foget to save!!!
		item_list = o.items.all() #Generate list of the items in the order
		# print Order.objects.filter(pk=request.user.id, order_status = 1) #TESTING IN RPEL

		#calculate the total price
		price = total_price(item_list)

		#render and pass in the data to html file and display
		return render(request, 'items/cart.html', {'item_list':item_list, 'price' : price})
		
# DELETE METHOD ALLOWS USER TO DELETE AN ITEM FROM CART
@login_required(login_url = login)
def delete(request, item_id):
	
	#find order for the signed in user
	o = Order.objects.filter(user=request.user, order_status = 1) 

	#identify item to delete from oder using the item ID passed into the function 
	i_delete = Items.objects.get(pk=item_id)
	o[0].items.remove(i_delete) #Remove the item from the items in the order
	item_list = o[0].items.all() #create an items list to pass into the dictionary

	#Calculate total price
	price = total_price(item_list)


	return render(request, 'items/cart.html', {'item_list':item_list, 'price' : price})

#PAYMENT METHOD ALLOWS USER TO ENTER PAYMENT INFORMATION
def payment(request):
	
	#find order for the user that has order_status = 1
	o = Order.objects.filter(user=request.user, order_status = 1) 
	item_list = o[0].items.all() #create an items list to pass into the dictionary

	#Calculate total price
	price = total_price(item_list)

	#Have a purchase status variable
	purchased = False

	return render(request, 'items/payment.html', {'item_list':item_list, 'price' : price, 'purchased' : purchased})

#PURCHASED METHOD CHANGED THE ORDER STATUS OF THE ITEMS TO 2 (PURCHASED)
def purchased(request):
	
	#find order for the user that has order_status = 1
	o = Order.objects.filter(user=request.user, order_status = 1) 
	item_list = o[0].items.all()#create an items list to pass into the dictionary
	
	#Calculate total price
	price = total_price(item_list)
	
	#Have a purchase status variable = True for the 'if' statement in the html file
	purchased = True

	return render(request, 'items/payment.html', {'item_list':item_list, 'price' : price, 'purchased': purchased}, )




