from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Review, ReviewImage
from .forms import ProductForm, ReviewForm, ReviewImageForm
# Create your views here.

def index(request):
    Products = Product.objects.order_by('-pk')
    context = {
        'Products': Products
    }
    return render(request, 'boss/index.html', context)

def detail(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    context = {
        'product': product,
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
def delete(request, artilce_pk):
    product = Product.objects.get(pk=artilce_pk)
    if request.user == product.user:
        product.delete()
    return redirect('boss:index')


@login_required
def create_review(request, product_pk):
    product = Product.objects.get(pk=product_pk)

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            for img in request.FILES.getlist('image'):
                image = ReviewImage()
                image.review = review
                image.image = img
                image.save()
            return redirect('boss:detail', product.pk)
    else:
        review_form = ReviewForm()
        reviewimage_form = ReviewImageForm()
    context = {
        'review_form': review_form,
        'reviewimage_form': reviewimage_form,
        'product': product,
    }
    return render(request, 'boss/create_review.html', context)
