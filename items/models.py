from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Items(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField(max_length=200)
	price = models.IntegerField(default = 0)

class Order(models.Model):
	order_status = models.IntegerField(default=0)
	items = models.ManyToManyField(Items)
	user = models.ForeignKey(User)

class Sandwich(models.Model):
	bread = models.CharField(max_length = 200)
	ingredient = models.CharField(max_length=200)
	


	# def __str__(self):
	# 	return self.items