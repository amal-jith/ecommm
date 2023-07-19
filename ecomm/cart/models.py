from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from store.models import Product

# Create your models here.


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    razor_pay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razor_pay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razor_pay_payment_signature = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return f"Cart - {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cart.user.username}'s Cart - {self.product.name}"




class Order(models.Model):
    billing_name = models.CharField(max_length=100)
    billing_email = models.EmailField()
    billing_address = models.TextField()
    billing_phone = models.CharField(max_length=20)
    shipping_name = models.CharField(max_length=100)
    shipping_address = models.TextField()
    card_number = models.CharField(max_length=16)
    card_expiry = models.CharField(max_length=10)
    card_cvv = models.CharField(max_length=4)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Order #{self.order.id} - {self.product.name}"