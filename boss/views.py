from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, F, Q, Avg, FloatField
from django.http import JsonResponse
from django.db.models.functions import Cast
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Product, Review, ReviewImage, Category, Subcategory
from .forms import ProductForm, ReviewForm, ReviewImageForm

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

    # boss/index_components/section.html에 들어갈 자료들
    titles = [
        '배달비품 BEST',
        #'믿고사는 식재료 BEST',
        '주방용품부터 배달용기까지',
        #'쟁여두면 좋은 식재료',
    ]
    subtitles = [
        '사장님들이 많이 찾는 배달비품 모음',
        #'고민은 배송만 늦출뿐',
        '홀도, 배달도 여기서 장사 준비해요',
        #'여기에서 만나보세요',
    ]

    #개당, g당 분리
    titles2 = [
        '믿고사는 식재료 BEST',
    ]
    subtitles2 = [
        '고민은 배송만 늦출뿐',
    ]

    #플러스1
    titles3 = [
        '플러스 원(+1) 기획전',
    ]
    subtitles3 = [
        '무조건 하나 더 드려요!',
    ]
    year_ago = timezone.now() - timedelta(days=365)
    best_products = Product.objects.annotate(
            num_orders=Count(
                'order',
                filter=Q(order__order_datetime__gt=year_ago)
            )
        ).order_by('-num_orders')
    
    delivery_prod_best = best_products.filter(
        subcategory__in=(
            16, 17, 18, 19, 20, 22, 26
        ),
        price__gt=F('sale_price')
    )
    ingredients_best = best_products.order_by('-id').filter(
        subcategory__in=(
            i for i in range(1, 16)
        )
    )[:12] 
    delivery_prod_all = Product.objects.all().order_by('-id').filter(
            subcategory__gte=16
    )
    one_plus_one_prod = Product.objects.all().filter(
        event__icontains = "1+1"
    )[:6]
    # print(one_plus_one_prod)


    #배달비품 기준단가 (개당) 계산
    delivery_prod_best_info = []
    #주방용품부터 배달용기까지
    delivery_prod_all_info = []
    for i in range(12):
        delivery_prod_best_info.append([delivery_prod_best[i], delivery_prod_best[i].get_discount_rate,delivery_prod_best[i].get_unit_price2])  
        delivery_prod_all_info.append([delivery_prod_all[i],delivery_prod_all[i].get_discount_rate,delivery_prod_all[i].get_unit_price2])
    
    #믿고사는 식재료 BEST 기준단가 (g당/개당) 분리 
    #weight이 0인 경우와 아닌 경우
    ingredients_best_info = []
    # print(ingredients_best[0].weight)
    for query in ingredients_best:
        #print(type(query)) #--> <class 'boss.models.Product'>
        if query.weight == 0: #개당
            ingredients_best_info.append([query,query.get_discount_rate,query.get_unit_price2,0])
        else:
            ingredients_best_info.append([query,query.get_discount_rate,query.get_unit_price,1])
    #1+1 (할인가 아닌것도 포함)
    one_plus_one_info = []
    for query in one_plus_one_prod:
        if query.weight == 0: #개당
            if query.sale_price<query.price:
                one_plus_one_info.append([query,query.get_discount_rate,query.get_unit_price2,0,"sale"])
            else:
                one_plus_one_info.append([query,query.get_discount_rate,query.get_unit_price2,0,"not-sale"])
        else:
            if query.sale_price<query.price:
                one_plus_one_info.append([query,query.get_discount_rate,query.get_unit_price,1,"sale"])
            else:
                one_plus_one_info.append([query,query.get_discount_rate,query.get_unit_price,1,"not-sale"])
    data = [
        # delivery_prod_best,
        delivery_prod_best_info,
        # ingredients_best,
        # ingredients_best_info,
        # Product.objects.filter(
        #     subcategory__gte=16
        # ),
        delivery_prod_all_info,
        # Product.objects.filter(
        #     Q(subcategory__lte=15) & Q(weight__gte=1000)
        # ),
    ]
    data2 = [
        ingredients_best_info,
    ]
    data3 = [
        one_plus_one_info,
    ]

    context = {
        'Products': Products,
        'discounted_info': discounted_info,
        'section_data': zip(titles, subtitles, data),
        'section_data2':zip(titles2,subtitles2,data2),
        'section_data3':zip(titles3,subtitles3,data3)
    }
    return render(request, 'boss/index.html', context)

  
def detail(request, product_pk):
    product = Product.objects.prefetch_related('review_set').get(pk=product_pk)
    context = {
        'product': product,
        'reviews': product.review_set.all(),
        'rating': round(product.review_set.aggregate(Avg('rating')).get('rating__avg'), 1),
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

def category_products(request, category_id):
    sort = request.GET.get('sort')
    category = get_object_or_404(Category, id=category_id)
    category_products = Product.objects.filter(category_id=category_id)
    if sort == '1':  # 무게당 가격
        category_products = category_products.annotate(unit_price=Cast(F('sale_price') / F('weight') * 100, output_field=FloatField())).order_by('unit_price')
    elif sort == '2': # 개당 가격
        category_products = category_products.annotate(unit_price=Cast(F('sale_price') / F('quantity') * 100, output_field=FloatField())).order_by('unit_price')
    else : #낮은 가격
        category_products = category_products.order_by('sale_price')
    product_count = category_products.count()  # 상품 개수
    context = {
        'category_name': category.name,
        'products': category_products,
        'product_count': product_count,
    }
    return render(request, 'boss/category_products.html', context)

def subcategory_products(request, subcategory_id):
    sort = request.GET.get('sort')
    category = get_object_or_404(Subcategory, id=subcategory_id)
    category_products = Product.objects.filter(subcategory_id=subcategory_id)
    if sort == '1':  # 무게당 가격
        category_products = category_products.annotate(unit_price=Cast(F('sale_price') / F('weight') * 100, output_field=FloatField())).order_by('unit_price')
    elif sort == '2': # 개당 가격
        category_products = category_products.annotate(unit_price=Cast(F('sale_price') / F('quantity') * 100, output_field=FloatField())).order_by('unit_price')
    else : #낮은 가격
        category_products = category_products.order_by('sale_price')
    product_count = category_products.count()  # 상품 개수
    context = {
        'category_name': category.name,
        'products': category_products,
        'product_count': product_count,
    }
    return render(request, 'boss/subcategory_products.html', context)