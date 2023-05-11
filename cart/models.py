from django.db import models
from boss.models import Product


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    added_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'Cart'
        ordering = ('added_at',)
    
    def __str__(self):
        return self.cart_id
    
    def total_amount(self):
        r = 0
        for cart_item in self.cartitem_set.all():
            r += cart_item.sub_total()
        return r
    

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'CartItem'
    
    def sub_total(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return self.product

