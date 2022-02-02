from django.conf.urls import url
from django.conf import settings
from django.views.static import serve
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    
    path('', views.index, name="index"),
    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('shop', views.store, name="shop"),
    
    path('register', views.register, name="register"),
	path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),

    path('shop/cart', views.cart, name="cart"),
    path('shop/checkout', views.checkout, name="checkout"),
    path('update_item', views.updateItem, name="update_item"),
	path('shop/process_order', views.processOrder, name="process_order"),

    path('myaccount/customer/<str:pk>', views.customer, name="customer"),
    path('myaccount/customer/view_order/<str:pk>', views.view_order, name="view_order"),

    path(
        'login/reset_password/',
        auth_views.PasswordResetView.as_view(template_name="templates/store/password_reset.html"),
        name="reset_password"
        ),
    path(
        'login/reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="templates/store/password_reset_sent.html"), 
        name="password_reset_done"
        ),
    path(
        #users id encored in base 64 and token to check if the password is valid
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name="templates/store/password_reset_form.html"), 
        name="password_reset_confirm"
        ),
    path(
        'login/reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="templates/store/password_reset_done.html"), 
        name="password_reset_complete"
        ),
]
