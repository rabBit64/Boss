from django.urls import path
from . import views

app_name = 'boss'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:product_pk>/', views.detail, name='detail'),
    path('<int:product_pk>/update_product/', views.update_product, name='update_product'),
]