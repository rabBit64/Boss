from django.urls import path
from . import views

app_name = 'kakaopay'
urlpatterns = [
    path('approval/<str:cart_id>/', views.approval, name='approval'),
    path('pay_fail/', views.pay_fail, name='pay_fail'),
    path('pay_cancel/', views.pay_cancel, name='pay_cancel'),
    path('wait/', views.wait, name='wait'),
    # path('pay_finish/<str:cart_id>/', views.pay_finish, name='pay_finsh'), # 필요없음
    path('<str:cart_id>/', views.pay, name='pay'), # 제일 아래에 위치
]
