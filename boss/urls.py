from django.urls import path
from . import views

app_name = 'boss'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:product_pk>/', views.detail, name='detail'),
    path('<int:product_pk>/update_product/', views.update_product, name='update_product'),
    path('<int:product_pk>/delete/', views.delete, name='delete'),
    path('<int:product_pk>/reviews/', views.review_create, name='review_create'),
    path('<int:product_pk>/reviews/<int:review_pk>/delete/', views.review_delete, name='review_delete'),
    path('<int:product_pk>/reviews/<int:review_pk>/update/', views.review_update, name='review_update'),
    path('search/', views.search, name='search'),
    path('<int:product_pk>/reviews/<int:review_pk>/likes/', views.review_likes, name='review_likes'),
    path('subcategory-options/', views.subcategory_options, name='subcategory_options'),
    path('category_products/<int:category_id>/', views.category_products, name='category_products'),
    path('subcategory_products/<int:subcategory_id>/', views.subcategory_products, name='subcategory_products'),
]