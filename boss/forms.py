from django import forms

from .models import Product, Review, ReviewImage, Category, Subcategory


class ProductForm(forms.ModelForm):
    name = forms.CharField(label='상품명', label_suffix='', widget=forms.TextInput(
        attrs={'class': 'form-control placeholder-font','style': 'width: 180px;', 'placeholder': '상품명 입력',}))
    
    weight = forms.IntegerField(label='무게', label_suffix='', widget=forms.NumberInput(
        attrs={'class': 'form-control placeholder-font','style': 'width: 180px;', 'placeholder': '무게 입력', }))

    country = forms.CharField(label='원산지', label_suffix='', widget=forms.TextInput(
        attrs={'class': 'form-control placeholder-font','style': 'width: 180px;', 'placeholder': '원산지 입력',}))
    
    quantity = forms.IntegerField(label='수량', label_suffix='', widget=forms.NumberInput(
        attrs={'class': 'form-control placeholder-font','style': 'width: 180px;', 'placeholder': '수량 입력', }))
    

    CATEGORIES= (
        ('가공식품', '가공식품'), 
        ('농수축산물', '농수축산물'), 
        ('배달용품', '배달용품'), 
        ('주방용품', '주방용품'), 
    )
    category = forms.ChoiceField(label='카테고리',
        widget=forms.Select(
            attrs={
                'class' : 'form-select mt-2',
                'style': 'width: 180px;',
            }
        ),
        choices=CATEGORIES)
    
    
    SUBCATEGORIES= (
        ('소시지/햄/육가공품', '소시지/햄/육가공품'), 
        ('차/음료/음료제조용', '차/음료/음료제조용'), 
        ('베이커리/디저트/스낵', '베이커리/디저트/스낵'), 
        ('조미료/소금/향신료', '조미료/소금/향신료'),
        ('소스/양념/육수', '소스/양념/육수'), 
        ('유제품', '유제품'), 
        ('튀김류/만두류/순대', '튀김류/만두류/순대'), 
        ('절임식품/반찬/김치류', '절임식품/반찬/김치류'),  
        ('가공기타', '가공기타'), 
        ('쌀', '쌀'), 
        ('잡곡/견과', '잡곡/견과'), 
        ('야채/채소', '야채/채소'), 
        ('축산/계란', '축산/계란'), 
        ('수산/건어물', '수산/건어물'), 
        ('과일', '과일'), 
        ('플라스틱용기', '플라스틱용기'), 
        ('종이용기/박스', '종이용기/박스'), 
        ('카페/음료/디저트 용품', '카페/음료/디저트 용품'), 
        ('종이/비닐봉투', '종이/비닐봉투'), 
        ('수저/위생용품', '수저/위생용품'),
        ('스티커/배너/포스터', '스티커/배너/포스터'), 
        ('포장재', '포장재'), 
        ('냄비/팬/뚝배기', '냄비/팬/뚝배기'), 
        ('식기/테이블웨어', '식기/테이블웨어'),
        ('조리도구', '조리도구'), 
        ('일회용품', '일회용품'), 
        ('주방잡화', '주방잡화'), 
        ('주방설비', '주방설비'),
    )
    subcategory = forms.ChoiceField(label='서브카테고리',
        widget=forms.Select(
            attrs={
                'class' : 'form-select mt-2',
                'style': 'width: 180px;',
            }
        ),
        choices=SUBCATEGORIES)
    
    price = forms.IntegerField(label='가격', required=True,
        widget=forms.NumberInput(
        attrs={'class': 'form-control placeholder-font','style': 'width: 180px;', 'placeholder': '가격 입력', }))

    sale_price = forms.IntegerField(
        label='판매가격',
        required=False,
        help_text='판매가격을 입력하지 않으시면 \'가격\'이 적용됩니다.',
        widget=forms.NumberInput(
        attrs={'class': 'form-control placeholder-font','style': 'width: 180px;', 'placeholder': '판매가격 입력', }))
    
 
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
