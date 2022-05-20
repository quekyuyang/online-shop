from django.conf import settings
from .models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product_id, quantity):
        product = Product.objects.get(id=product_id)
        self.cart[str(product_id)] = {
        'name': product.name,
        'quantity': quantity,
        'price': product.price*quantity
        }
        self.session.modified = True

    def remove(self, product_id):
        del self.cart[str(product_id)]
        self.session.modified = True

    def total_price(self):
        total_price = 0
        for entry in self.cart.values():
            total_price += entry['price']
        return total_price

    def __iter__(self):
        cart = self.cart.copy()
        products = Product.objects.filter(id__in=cart.keys())

        for product in products:
            cart[str(product.id)]['product'] = product
            yield cart[str(product.id)]
