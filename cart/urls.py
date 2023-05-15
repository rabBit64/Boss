from django.urls import path
from . import views


app_name = 'cart'

urlpatterns = [
    path('add/<int:product_pk>/', views.add_cart, name='add_cart'),
    path('', views.cart_detail, name='cart_detail'),
    path('increase_item/<int:product_pk>/', views.increase_item, name='increase_item'),
    path('decrease_item/<int:product_pk>/', views.decrease_item, name='decrease_item'),
    path('remove_item/<int:product_pk>/', views.remove_item, name='remove_item'),
]