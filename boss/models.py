from django.db import models
from django.conf import settings

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)


class Subcategory(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')


class DetailCategory(models.Model):
    name = models.CharField(max_length=50)
    Subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='detailcategory')

class Product(models.Model):
    name = models.CharField(max_length=100)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_users')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='subcategory')
    weight = models.IntegerField() # 중량
    quantity = models.IntegerField() # 수량
    country = models.CharField(max_length=50) # 제조국


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='review')
    content = models.TextField()


