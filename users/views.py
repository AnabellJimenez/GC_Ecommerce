from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# USERS METHOD REDIRECTS TO REGISTER PAGE
def users(request):
	return render(request, 'users/register.html')

#SIGN_UP METHOD SAVES REGISTERED USER INFO AND REDIRECTS TO LOGIN
def sign_up(request):
	#save name, email and password from the html form
	name = request.POST["user_name"]
	email = request.POST["email"]
	password = request.POST["password"]

	#create user using the Django User built in model
	user = User.objects.create_user(username=name,email=email,password=password)
	#save new user created
	user.save() 
	#render to login page
	return render(request, 'users/login.html')

#LOG_IN  METHOD PROVIDES FORM FOR USERS TO ENTER THEIR LOGIN INFORMATION
def log_in(request):
	return render(request, 'users/login.html')

#VERIFY METHOD USES THE DJANGO BUILT IN AUTHENTICATE TO VERIFY THE USER
def verify(request):
	#save the user input from the login form
	username = request.POST["username"]
	password = request.POST["password"]

	#verify the user is valid using autenticate
	user = authenticate(username = username, password = password)

	#if there is a user entered (not empty fields)
	if user is not None:
		if user.is_active:
			login(request, user)#use the login imported method to verify the user
			#allow user to access member only page
			return HttpResponseRedirect(reverse('users:home')) 
		else: 
			return HttpResponse("ACCOUNT ERROR")
	else:
		return HttpResponse("INVALID LOGIN")

#INDEX METHOD REDIRECTS TO AN INDEX PAGE
def index(request):
	return render(request, 'users/index.html')

#HOME METHOD ALLOWS MEMBERS ACCESS IF THEY ARE VALID USERS
def home(request):
	#print request.user #CODE FOR TESTING 

	if request.user.is_authenticated():
		return render(request, 'users/home.html')
	else:
		return HttpResponse("CANNOT ACCESS PAGE")

#LOG_OUT METHOD LOGS OUT USER
def log_out(request):
	logout(request)
	return render(request, 'users/index.html')





