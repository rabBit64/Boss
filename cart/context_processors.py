from .models import Cart, CartItem
from .views import _cart_id


def counter(request):
    item_count = 0
    try:
        cart = Cart.objects.filter(cart_id=_cart_id(request))
        cart_items = CartItem.objects.all().filter(cart=cart[:1])
        item_count = len(cart_items)
    except Cart.DoesNotExist:
        item_count = 0
    
    context = {
        'item_count': item_count,
    }
    return context
