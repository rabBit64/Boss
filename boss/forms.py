from django import forms

from .models import Product, Review, ReviewImage, Category, Subcategory


class ProductForm(forms.ModelForm):
    price = forms.IntegerField(label='가격', required=True)
    sell_price = forms.IntegerField(
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
            'sell_price',
        )
    
    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        sell_price = cleaned_data.get('sell_price')
        if not sell_price or sell_price is None:
            cleaned_data['sell_price'] = sell_price = price
        if sell_price > price:
            raise forms.ValidationError('판매가격은 기존 가격보다 낮아야 합니다.')
        return cleaned_data
        

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
