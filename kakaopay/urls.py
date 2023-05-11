from django.urls import path
from . import views

app_name = 'kakaopay'
urlpatterns = [
    path('approval/<str:cart_id>/', views.approval, name='approval'), # 카트아이디
    path('pay_fail/', views.pay_fail, name='pay_fail'),
    path('pay_cancel/', views.pay_cancel, name='pay_cancel'),
    path('<str:cart_id>/', views.pay, name='pay'), # 제일 아래에 위치
]
