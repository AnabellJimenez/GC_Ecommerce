from django.conf.urls import url
from . import views

urlpatterns = [
url(r'^$', views.items, name='items'),
# url(r'^', views.items, name='items'),
url(r'^(?P<item_id>[0-9]+)/$', views.show, name = 'show'),
# url(r'^cart', views.cart, name = 'cart'),
url(r'^cart/(?P<item_id>[0-9]+)/$', views.cart, name = 'cart'),
url(r'^delete/(?P<item_id>[0-9]+)/$', views.delete, name = 'delete'),
url(r'^payment', views.payment, name = 'payment'),
url(r'^purchased', views.purchased, name = 'purchased'),

]
