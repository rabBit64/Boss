from django import forms
from .models import Product, Review


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('content',)
