from django.conf.urls import url
from django.conf import settings
from django.views.static import serve
from django.urls import path
from . import views


urlpatterns = [
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

    path('home', views.dashboard, name="dashboard"),
    path('distributors', views.distributors, name="distributors"),
    path('customers', views.customers_table, name="customers"),
    path('products', views.products, name="products"),
    path('messages', views.customerMessages, name="messages"),


    path('add_distributor', views.CreateDistributor, name="add_distributor"),
    path('add_product', views.AddProduct, name="add_product"),

    path('view_order/<str:pk>', views.ViewOrder, name="view_order"),
    path('view_product/<str:pk>', views.ViewProduct, name="view_product"),
    path('view_customer/<str:pk>', views.ViewCustomer, name="view_customer"),
    path('view_message/<str:pk>', views.ViewMessage, name="view_message"),


    path('delete/<str:pk>/', views.delete_Order, name="delete"),
    path('delete_distributor/<str:pk>/', views.deleteDistributor, name="delete_distributor"),
    path('delete_customer/<str:pk>/', views.deleteCustomer, name="delete_customer"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
    path('delete_product/<str:pk>/', views.deleteProduct, name="delete_product"),
     path('delete_message/<str:pk>/', views.deleteMessage, name="delete_message"),



]