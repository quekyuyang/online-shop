from django.conf import settings
from .models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add_product(self, product_id, quantity):
        product = Product.objects.get(id=product_id)
        self.cart[str(product_id)] = {
        'name': product.name,
        'quantity': quantity,
        'price': product.price*quantity
        }
        self.session.modified = True
