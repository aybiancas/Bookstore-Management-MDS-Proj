from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('products/', views.products, name='products'),
    path('add-book/', views.add_book, name='add_book'),
    path('sales/', views.sales, name='sales'),
    path('users/', views.users, name='users'),
    path('logout/', views.logout_view, name='logout')
]