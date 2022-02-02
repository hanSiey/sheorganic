from django.shortcuts import render,redirect
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder
from .forms import *
from django.contrib.auth.models import Group, User, auth
from django.contrib.auth import authenticate
from django.contrib import messages
from .decorators import unauthenticated_user
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

# Create your views here.

def index(request):
		if request.user.is_superuser :
			return redirect('dashboard')
		else:
			return render(request, "store/index.html")

def about(request):
		if request.user.is_superuser :
			return redirect('dashboard')
		else:
			return render(request, "store/about.html")
		
def contact(request):
		if request.user.is_superuser :
			return redirect('dashboard')
		else:
			if request.method == "POST":
				message_form = messageform(request.POST)
				if message_form.is_valid():
					message_form.save()
					return redirect('/')
				else:
					messages.info(request, "Enter valid information")
					return redirect('contact')
			else:
				message_form = messageform()

			context = {
				'form':message_form
			}
			return render(request, "store/contact.html", context)

@unauthenticated_user
def register(request):
		if request.method == 'POST':
			create_user_form = CreateUser(request.POST)

			if create_user_form.is_valid():
				name = create_user_form.cleaned_data.get('name')
				surname = create_user_form.cleaned_data.get('surname')
				email = create_user_form.cleaned_data.get('email')
				phone = create_user_form.cleaned_data.get('phone')
				password1 = create_user_form.cleaned_data.get('password1')
				password2 = create_user_form.cleaned_data.get('password2')

				if password1 == password2:
					if User.objects.filter(email=email).exists():
						messages.info(request, 'Email Already exists')
						return redirect('register')
					elif User.objects.filter(username=name, email=email).exists():
						messages.info(request, 'User Already exists')
						return redirect('register')
					else:
						user = User.objects.create_user(username=name, email=email,first_name=name, last_name=surname, password=password1)
						user.save()
						
						group = Group.objects.get(name="customer")
						user.groups.add(group)
					
					new_user = User.objects.get(email=email)
					Customer.objects.create(
						user=new_user,
						name=new_user.first_name,
						surname=new_user.last_name,
						email=new_user.email,
						phone=phone,
					)
					messages.info(request, "Account successfully created")
					return redirect('login')
				else:
					messages.info(request, 'Passwords Do Not Match')
					return redirect('register')
		else:
			create_user_form = CreateUser() 
		return render(request, 'store/register.html', {'form':create_user_form})

@unauthenticated_user
def login(request):
		if request.method == 'POST':
			login_form = LogInForm(request.POST)

			username = request.POST.get('name')
			email =request.POST.get('email')
			password =request.POST.get('password1')

			user = authenticate(request, username=username, email=email, password=password)
			if user is not None:
				auth.login(request, user)
				if user.is_superuser:
					return redirect('dashboard')
				else:
					return redirect('/')
			else:
				messages.info(request, 'Credentails invalid')
				return redirect('login')     
		else:
			login_form = LogInForm()
		return render(request, 'store/login.html', {'form':login_form})

def logout(request):
		auth.logout(request)
		return redirect('/')
		
def store(request):
		if request.user.is_superuser :
			return redirect('dashboard')
		else:
			data = cartData(request)

			cartItems = data['cartItems']
			order = data['order']
			items = data['items']

			products = Product.objects.all()
			context = {'products':products, 'cartItems':cartItems}
			return render(request, 'store/shop.html', context)


def cart(request):
		if request.user.is_superuser :
			return redirect('dashboard')
		else:
			data = cartData(request)

			cartItems = data['cartItems']
			order = data['order']
			items = data['items']

			context = {'items':items, 'order':order, 'cartItems':cartItems}
			return render(request, 'store/cart.html', context)

def checkout(request):
		if request.user.is_superuser :
			return redirect('dashboard')
		else:
			checkout_form = CheckoutForm()
			data = cartData(request)
			cartItems = data['cartItems']
			order = data['order']
			items = data['items']

			context = {
				'items':items, 
				'order':order, 
				'cartItems':cartItems,
				'form':checkout_form,
			}
			return render(request, 'store/checkout.html', context)

def updateItem(request):
		data = json.loads(request.body)

		productId = data['productId']
		action = data['action']

		customer = request.user.customer
		
		product = Product.objects.get(id=productId)
		order, created = Order.objects.get_or_create(customer=customer, complete=False)

		orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
		
		if action == 'add':
			orderItem.quantity = (orderItem.quantity + 1)
		elif action == 'remove':
			orderItem.quantity = (orderItem.quantity - 1)

		orderItem.save()

		if orderItem.quantity <= 0:
			orderItem.delete()

		return JsonResponse('Item was added', safe=False)


def processOrder(request):
		transaction_id = datetime.now().timestamp()
		data = json.loads(request.body)

		if request.user.is_authenticated:
			customer = request.user.customer
			order, created = Order.objects.get_or_create(customer=customer, complete=False)
		else:
			customer, order = guestOrder(request, data)

		total = float(data['form']['total'])
		order.transaction_id = transaction_id

		if total == order.get_cart_total:
			order.complete = True
		order.save()

		if order.shipping == True:
			ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode'],
			)

		context = {
			'name': order.customer.name,
			'surname':order.customer.surname,
			'total': total,
			'items': order.get_cart_items,
		}

		template_admin = render_to_string('templates/store/order_info_email.html', context)
		email_admin = EmailMessage(
			'New Order',
			template_admin,
			settings.EMAIL_HOST_USER,
			['Shebeautyandorganics@gmail.com']
		)
		email_admin.fail_silently = False
		email_admin.send()

		template_customer = render_to_string('templates/store/order_confirmation_email.html', context)
		email_customer = EmailMessage(
			'Order Confirmation',
			template_customer,
			settings.EMAIL_HOST_USER,
			[str(order.customer.email)]
		)
		email_customer.fail_silently = False
		email_customer.send()
		return JsonResponse('Order Placed..', safe=False)

def customer(request, pk):
		if request.user.is_superuser :
			return redirect('dashboard')
		else:
			customer = Customer.objects.get(id=pk)
			orders = customer.order_set.all().filter(complete=True).order_by('-id')
			orders_count = orders.count()
			
			context = {
				'customer':customer,
				'orders': orders,
				'total':orders_count,
			}
			return render(request, "store/customer.html", context)

def view_order(request, pk):
		order = Order.objects.get(id=pk)
		items = order.orderitem_set.all()
		addresses = order.shippingaddress_set.all()

		context = {
			'order':order,
			'items':items,
			'addresses':addresses,
		}
		return render(request, "store/view_order.html", context)



