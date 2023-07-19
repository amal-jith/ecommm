from decimal import Decimal
from django.conf import settings
from store.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get(settings.CART_SESSION_ID)
        if not self.cart:
            self.cart = self.session[settings.CART_SESSION_ID] = {}

    def add(self, product_id, quantity=1):
        product = Product.objects.get(id=product_id)
        product_id = str(product_id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    def get_total_price(self):
        total_price = sum(
            Decimal(item['price']) * item['quantity'] for item in self.cart.values()
        )
        return total_price

    def get_items(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart_items = []

        for product in products:
            cart_items.append(
                {
                    'product': product,
                    'quantity': self.cart[str(product.id)]['quantity'],
                    'get_total_price': Decimal(self.cart[str(product.id)]['price'])
                    * self.cart[str(product.id)]['quantity'],
                }
            )

        return cart_items

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def update_total_price(self):
        pass
