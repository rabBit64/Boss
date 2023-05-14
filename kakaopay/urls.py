from django.urls import path
from . import views

app_name = 'kakaopay'
urlpatterns = [
    path('wait/', views.wait, name='wait'),
    path('pay/<str:cart_id>/', views.pay, name='pay'),
    path('approval/<str:cart_id>/', views.approval, name='approval'),
    path('pay_fail/', views.pay_fail, name='pay_fail'),
    path('pay_cancel/', views.pay_cancel, name='pay_cancel'),

    path('wait_product/', views.wait_product, name='wait_product'),
    path('pay_product/<int:product_pk>/<int:count>/', views.pay_product, name='pay_product'),
    path('approval_product/<int:product_pk>/<int:count>/', views.approval_product, name='approval_product'),
    path('pay_product_fail/', views.pay_product_fail, name='pay_product_fail'),
    path('pay_product_cancel/', views.pay_product_cancel, name='pay_product_cancel'),
]
