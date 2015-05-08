from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^index', views.index, name='index'),
	url(r'^$', views.users, name='users'),
	url(r'^sign_up', views.sign_up, name = 'sign_up'),
	url(r'^log_in', views.log_in, name='log_in'),
	url(r'^verify', views.verify, name='verify'),
	url(r'^home', views.home, name='home'),
	url(r'^log_out', views.log_out, name='log_out'),

]

