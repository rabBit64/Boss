from django import forms

from .models import Product, Review, ReviewImage, Category, Subcategory


class ProductForm(forms.ModelForm):
    price = forms.IntegerField(label='가격', required=True)
    sale_price = forms.IntegerField(
        label='판매가격',
        required=False,
        help_text='판매가격을 입력하지 않으시면 \'가격\'이 적용됩니다.',
    )

    class Meta:
        model = Product
        fields = (
            'name',
            'weight',
            'country',
            'quantity',
            'image',
            'category',
            'subcategory',
            'price',
            'sale_price',
        )
        

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('content',)


class ReviewImageForm(forms.ModelForm):
    image = forms.ImageField(
        widget = forms.ClearableFileInput(
            attrs = {
                'multiple': True,
            },
        ),
        required=False,
    )
    class Meta:
        model = ReviewImage
        fields = ('image',)
