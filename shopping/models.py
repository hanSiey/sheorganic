from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=20, null=True)
	surname = models.CharField(max_length=20, null=True)
	email = models.CharField(max_length=200)
	phone = models.CharField(max_length=15, null=True)

	def __str__(self):
		return self.name


class Product(models.Model):
	STATUS = (
		('Available', 'Available'),
		('Out of Stock', 'Out of Stock'),
	)
	name = models.CharField(max_length=200)
	price = models.FloatField()
	measurement = models.CharField(max_length=10)
	status = models.CharField(max_length=20, blank=True, choices=STATUS, default="Available")
	image = models.ImageField(null=True,blank=True)

	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

class Order(models.Model):
	STATUS = (
		('Pending', 'Pending'),
		('Out on delivery', 'Out on delivery'),
		('Delivered', 'Delivered')
	)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
	date_ordered = models.DateTimeField(default=datetime.now)
	status = models.CharField(max_length=20, blank=True, choices=STATUS, default="Pending")
	complete = models.BooleanField(default=False) #updates cart state
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.customer.name)
		
	@property
	def shipping(self):
		return True

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(default=datetime.now, blank=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(default=datetime.now, blank=True)

	def __str__(self):
		return self.address

class ClientMessage(models.Model):
	name = models.CharField(max_length=100)
	surname = models.CharField(max_length=60)
	email = models.EmailField()
	message = models.CharField(max_length=10000000)
	date_sent = models.DateTimeField(default=datetime.now, blank=True)
