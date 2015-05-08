from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
# Create your views here.

def users(request):
	return render(request, 'users/register.html')

def sign_up(request):
	name = request.POST["user_name"]
	email = request.POST["email"]
	password = request.POST["password"]

	user = User.objects.create_user(username=name,email=email,password=password)
	user.save() 
	return render(request, 'users/login.html')

def log_in(request):
	return render(request, 'users/login.html')

def verify(request):
	username = request.POST["username"]
	password = request.POST["password"]
	user = authenticate(username = username, password = password)
	if user is not None:
		if user.is_active:
			login(request, user)
			return HttpResponseRedirect(reverse('users:home'))
		else: 
			return HttpResponse("ACCOUNT ERROR")
	else:
		return HttpResponse("INVALID LOGIN")

def index(request):
	return render(request, 'users/index.html')

def home(request):
	print request.user

	if request.user.is_authenticated():
		return render(request, 'users/home.html')
	else:
		return HttpResponse("CANNOT ACCESS PAGE")

def log_out(request):
	logout(request)
	return render(request, 'users/index.html')





