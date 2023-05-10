from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Review
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
        return redirect('boss:detail', product.pk)
    context = {
        'product': product,
        'review_form': review_form,
        'reviewimage_form': reviewimage_form
    }
    return render(request, 'boss/detail.html', context)

@login_required
def review_delete(request, product_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.user:
        review.delete()

    return redirect('boss:detail', product_pk)
