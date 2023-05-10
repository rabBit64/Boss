from django.urls import path
from . import views

app_name = 'boss'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:product_pk>/', views.detail, name='detail'),
    path('<int:product_pk>/update_product/', views.update_product, name='update_product'),
    path('<int:product_pk>/delete/', views.delete, name='delete'),
    path('<int:product_pk>/create/', views.create_review, name='create_review'),
    path('<int:product_pk>/<int:review_pk>/delete/', views.delete_review, name='delete_review'),
]