from django import forms
from .models import Product, Review, ReviewImage


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name','weight','country','quantity','image','category','subcategory','price',)
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('content',)

class ReviewImageForm(forms.ModelForm):
    class Meta:
        model = ReviewImage
        fields = ('image',)