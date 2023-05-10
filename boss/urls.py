from django.urls import path
from . import views
app_name = 'boss'
urlpatterns = [
    path('',views.index,name='index'),
]