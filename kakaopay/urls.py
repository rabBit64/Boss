from django.urls import path
from . import views

app_name = 'kakaopay'
urlpatterns = [
    path('', views.index, name='index'),
    path('kakaopay/', views.kakaopay, name='kakaopay'), # 카트아이디
    path('pay_success/', views.pay_success, name='pay_success'), # 카트아이디
    path('pay_fail/', views.pay_fail, name='pay_fail'),
    path('pay_cancel/', views.pay_cancel, name='pay_cancel'),
]
