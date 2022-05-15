from django.conf import settings
from .models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add_product(self, product_id, quantity, price):
        self.cart[str(product_id)] = {'quantity': quantity, 'price': price}
        self.session.modified = True
