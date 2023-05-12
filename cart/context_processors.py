from .models import Cart, CartItem
from .views import _cart_id


def counter(request):
    item_count = 0
    # try:
    #     cart = Cart.objects.get(cart_id=_cart_id(request))
    # except Cart.DoesNotExist:
    #     cart = Cart.objects.create(cart_id = _cart_id(request))
    #     cart.save()
    # if 'admin' in request.path:
    #     return {}
    # else:
    try:
        cart = Cart.objects.filter(cart_id=_cart_id(request))
        print('@@@@@@@@@@@@@@@@@@@@@@@@', cart)
        # print(Cart.objects.all())
        cart_items = CartItem.objects.all().filter(cart=cart[:1])
        # print(len(cart_items))
        item_count = len(cart_items)
        # print(len(cart.cartitem_set.all()))
        # cart_items = Cart.objects.all().filter(cart=cart[:1])
        # for cart_item in cart_items:
        #     item_count += cart_item.quantity
    except Cart.DoesNotExist:
        item_count = 0
    
    context = {
        'item_count': item_count,
    }
    return context
    # return

from datetime import datetime

def current_datetime(request):
    context = {
        'current_datetime': datetime.now(),
    }
    return context