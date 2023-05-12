from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    def get_upload_path(instance, filename):
        return f'products/{instance.user.username}/{instance.name}/{filename}'
      
    name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_products', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to=get_upload_path, blank=True)
    weight = models.IntegerField(validators=[MinValueValidator(1)])  # 중량
    quantity = models.IntegerField(default=1) # 수량
    country = models.CharField(max_length=50) # 제조국
    price = models.IntegerField(validators=[MinValueValidator(1)])  #상품가격
    sale_price = models.IntegerField()
    
    #### 모델 할인율, 1+1 상품 여부, 무료배송 여부 추가
    # discount_rate = models.IntegerField(default=0)
    delivery_fee = models.IntegerField(default=0)

    # 쿠폰팩, 기획전, 1+1 등 이벤트를 CharField로 기록
    event = models.CharField('이벤트', max_length=50, blank=True, default='')

    
    def __str__(self):
        return self.name
    
    
    def clean(self):
        '''
        sale_price가 price보다 큰 값일 때 ValidationError 발생
        sale_price를 입력하지 않았을 때 sale_price에 price 입력
        '''
        if self.sale_price is None or not self.sale_price:
            self.sale_price = self.price
        if self.sale_price > self.price:
            raise ValidationError('판매가격은 기존 가격보다 낮아야 합니다.')
        super().clean()

    #할인율 계산
    @property  #데코레이터는 메소드를 마치 필드인 것처럼 취급할 수 있도록 만들어 준다
    def get_discount_rate(self):
        before_price = self.price
        after_price = self.sale_price
        if after_price==0:
            return 0
        else:
            # (할인액 / 정가) X 100
            return round(((before_price-after_price) / before_price) * 100)

    #기준단가 계산 (100g당)
    @property
    def get_unit_price(self):
        on_sale = False
        unit_price = 0
        if self.sale_price!=0:
            on_sale=True
        #할인되는 경우와 그렇지 않은 경우 나눠서 계산
        if on_sale:
            unit_price = (self.sale_price / self.weight) * 100
        else:
            unit_price = (self.price / self.weight) * 100
        return int(unit_price)



class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews', blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    image = models.ImageField(blank=True)


class IndexCarouselImage(models.Model):
    image = models.ImageField('carousel_image', upload_to='carousel')
    order = models.IntegerField('순서', default=0)

    def __str__(self):
        return self.image.name
    