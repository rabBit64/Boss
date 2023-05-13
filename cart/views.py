from django.shortcuts import render, redirect, get_object_or_404
from boss.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist


# 세션 key
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


# 카트 추가
def add_cart(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = _cart_id(request))
        cart.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart
        )
        cart_item.save()
    return redirect('boss:detail', product.pk)


# 카트 상세
def cart_detail(request, total=0, counter=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = _cart_id(request))
        cart.save()
    try:
        cart_items = CartItem.objects.filter(cart=cart, active=True).order_by('product__user')
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'counter': counter,
        'cart': cart,
    }

    return render(request, 'cart/cart.html', context)


# 상품 수량 증가
def increase_item(request, product_pk): 
    product = Product.objects.get(pk=product_pk)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart
        )
        cart_item.save()
    return redirect('cart:cart_detail')


# 상품 수량 감소
def decrease_item(request, product_pk):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, pk=product_pk)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('cart:cart_detail')


# 상품 제거
def remove_item(request, product_pk):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, pk=product_pk)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart:cart_detail')
