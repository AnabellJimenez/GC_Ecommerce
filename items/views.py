from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from items.models import Items, Order
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from django.core import serializers
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

# Create your views here.
def items(request):
	# items_list = Items.objects.all()
	# return render(request, 'items/Item_list.html', {'items_list': items_list})
	items_list = Items.objects.all()
	# objects = []
	# for items in items_list:
	# 	objects.append(items.name)
	if request.GET.get('search'):
		items_list = Items.objects.filter(name__contains=request.GET.get('search'))
	if request.GET.get('price') == "1":
		items_list = items_list.filter(price__lte=25)
	if request.GET.get('price') == "2":
		items_list = items_list.filter(price__gte=25, price__lte=200)
	if request.GET.get('price') == "3":
		items_list = items_list.filter(price__gte=200)


	paginator = Paginator(items_list, 4)

	page = request.GET.get('page')
	try:
		items = paginator.page(page)
	except PageNotAnInteger:
		items = paginator.page(1)
	except Emptypage:
		items = paginator.page(paginator.num)


	# return render_to_response('items/items.html', {"items": items})
	
	if request.GET.get('format') == 'json':
		data = serializers.serialize("json", items)
		return HttpResponse(data, content_type='application/json')
	else:
		return render_to_response('items/items.html', {"items": items})

def show(request, item_id):

	status = int(len(Items.objects.filter(id = item_id)))
	print status

	try:
		item = Items.objects.get(pk=item_id)
	except Items.DoesNotExist:
		return HttpResponse("ITEM DOES NOT EXIST")

	return render(request, 'items/show.html', {'item': item, 'item_id': item_id, 'status': status})

def cart(request, item_id):
	
	# verify user?
	print "USERNAME: " , user.username
	if not request.user.is_authenticated():
		return HttpResponse("CANNOT ACCESS PAGE")

	#Does user have order?
	o = Order.objects.filter(pk=request.user.id, order_status = 1)
	# print o

	if o:
		print "added item to order"
		o[0].user = request.user
		o[0].save() 
		o[0].items.add(Items.objects.get(pk=item_id))
		o[0].save()
		item_list = o[0].items.all()
		print "item list: \n", o[0].items.all()
		return render(request, 'items/cart.html', {'item_list':item_list})
		
	else:
		o = Order()
		print "\nnew order created\n"
		return HttpResponse("new order created")
		# o.order_status = 1
		# o.user = request.user
		# o.save()
		# o.items.add(Items.objects.get(pk=item_id))
		# o.save()
		# item_list = o.items.all()
		# return render(request, 'items/cart.html', {'item_list':item_list})
		

def delete(request, item_id):
	pass
# 	o = Order.objects.filter(pk=request.user.id, order_status = 1)
# 	print o
# 	# o[0].items. = request.user
# 	# o[0].save()
# 	# i_delete = Items.objects.get(item_id)
# 	# print i_delete
# 	return HttpResponse("item to delete")
# 	# o[0].save()
# 	# item_list = o[0].items.all()
# 	# return render(request, 'items/cart.html', {'item_list':item_list})



