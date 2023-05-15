import os
from django.conf import settings
from django.db.models import F
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Review, ReviewImage, IndexCarouselImage, Category, Subcategory
from .forms import ProductForm, ReviewForm, ReviewImageForm
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Q, F, FloatField
from django.db.models.functions import Cast
def index(request):
    Products = Product.objects.order_by('-pk')[:6]

    #할인된 제품만 넘기기
    discounted_info = []
    # discounted_products = Product.objects.exclude(sale_price = 0)[:6]
    discounted_products = Product.objects.filter(price__gt=F('sale_price')).exclude(sale_price=0)[:6]
    # print(discounted_products[0].get_discount_rate)
    #print(discounted_products[0].get_unit_price)
    for i in range(6):
       discounted_info.append([discounted_products[i],discounted_products[i].get_discount_rate,discounted_products[i].get_unit_price])
    print(discounted_info)
    context = {
        'Products': Products,
        'discounted_info': discounted_info,
    }
    return render(request, 'boss/index.html', context)

def detail(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    reviews = Review.objects.filter(product=product)
    context = {
        'product': product,
        'reviews': reviews,
        }
    return render(request, 'boss/detail.html', context)

@login_required
def create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('boss:detail', product_pk=product.pk)
    else:
        form = ProductForm()
    context = {
        'form': form,
    }
    return render(request, 'boss/create.html', context)

@login_required
def update_product(request, product_pk):
    product = Product.objects.get(pk=product_pk)

    if request.user == product.user:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                return redirect('boss:detail', product_pk=product.pk)
        else:
            form = ProductForm(instance=product)
    else:
        return redirect('boss:index')
    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'boss/update_product.html', context)

@login_required
def delete(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    if request.user == product.user:
        product.delete()
    return redirect('boss:index')

@login_required
def review_create(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    review_form = ReviewForm(request.POST)
    reviewimage_form = ReviewImageForm(request.POST)
    if review_form.is_valid():
        review = review_form.save(commit=False)
        review.product = product
        review.user = request.user
        review.save()
        for img in request.FILES.getlist('image'):
            image = ReviewImage()
            image.review = review
            image.image = img
            image.save()
        return redirect('boss:detail', product.pk)
    context = {
        'product': product,
        'review_form': review_form,
        'reviewimage_form': reviewimage_form
    }
    return render(request, 'boss/review_create.html', context)

@login_required
def review_delete(request, product_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.user:
        review.delete()
    return redirect('boss:detail', product_pk)
  
@login_required
def review_update(request, product_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    images = review.reviewimage_set.all()
    if request.user != review.user:
        return redirect('boss:detail', product_pk)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST, request.FILES, instance=review)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.save()
            for img in request.FILES.getlist('image'):
                image = ReviewImage()
                image.review = review
                image.image = img
                image.save()
            images_to_delete = request.POST.getlist('delete_images')
            for image_pk in images_to_delete:
                image = ReviewImage.objects.get(pk=image_pk)
                image.delete()
            return redirect('boss:detail', product_pk)
    else:
        form = ReviewForm(instance=review)
        reviewimage_form = ReviewImageForm()
    context = {
        'form': form,
        'reviewimage_form': reviewimage_form,
        'images': images,
        'review': review,
    }
    return render(request, 'boss/review_update.html', context)
  


def search(request):
    keyword = request.GET.get('keyword')
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')
    min_price = request.GET.get('min_price')
    delivery_fee_zero = request.GET.get('delivery_fee_zero')
    discount = request.GET.get('discount')
    sort = request.GET.get('sort')
    q = Q()
    q &= Q(name__contains=keyword)

    if category_id:
        category = get_object_or_404(Category, id=category_id)
        q &= Q(category=category)

    if subcategory_id:
        subcategory = get_object_or_404(Subcategory, id=subcategory_id)
        q &= Q(subcategory=subcategory)

    if delivery_fee_zero == '1':  # delivery_fee_zero 값이 1인 경우 필터링
        q &= Q(delivery_fee=0)
    if discount == '1': 
        q &= Q(sale_price__lt=F('price')) 
    if min_price:
        # Apply price range filtering
        min_price = int(min_price)
        if min_price < 7000:
            q &= Q(sale_price__lt=7000)
        elif min_price < 15000:
            q &= Q(sale_price__gte=7000, sale_price__lt=15000)
        elif min_price < 30000:
            q &= Q(sale_price__gte=15000, sale_price__lt=30000)
        elif min_price < 50000:
            q &= Q(sale_price__gte=30000, sale_price__lt=50000)
        elif min_price < 100000:
            q &= Q(sale_price__gte=50000, sale_price__lt=100000)    
        else:
            q &= Q(sale_price__gte=100000)

    categories = Category.objects.all()[:4]
    subcategories = Subcategory.objects.all()
    products = Product.objects.filter(q)

    if sort == '1':  # 무게당 가격
        products = products.annotate(unit_price=Cast(F('sale_price') / F('weight') * 100, output_field=FloatField())).order_by('unit_price')
    elif sort == '2': # 개당 가격
        products = products.annotate(unit_price=Cast(F('sale_price') / F('quantity') * 100, output_field=FloatField())).order_by('unit_price')
    else : #낮은 가격
        products = products.order_by('sale_price')
    len_element = 100
    paginator = Paginator(products, len_element)
    page_number = request.GET.get('page')

    if page_number is None:
        page_number = 1
    page_obj = paginator.get_page(page_number)
    len_page = (len(products) + 1) // len_element
    pages = range(1, len_page + 1)
    filtered_product_count = products.count()  # 필터링된 상품 개수

    context = {
        'products': page_obj,
        'keyword': keyword,
        'pages': pages,
        'page_number': int(page_number),
        'categories': categories,
        'subcategories': subcategories,
        'filtered_product_count': filtered_product_count,  # 필터링된 상품 개수 전달
        'min_price': min_price,

    }
    return render(request, 'boss/search.html', context)

def subcategory_options(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id)

    options = '<option value="">---------</option>'
    for subcategory in subcategories:
        options += f'<option value="{subcategory.id}">{subcategory.name}</option>'

    return JsonResponse({'options': options})

@login_required
def review_likes(request, product_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if review.like_users.filter(pk=request.user.pk).exists():
        review.like_users.remove(request.user)
    else:
        review.like_users.add(request.user)
    return redirect('boss:detail', product_pk)
