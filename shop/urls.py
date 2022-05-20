from django.urls import path
from . import views


urlpatterns = [
    path('add_product', views.add_product, name='add_product'),
    path('cart', views.cart, name='cart'),
    path('remove_from_cart/<int:product_id>', views.remove_from_cart, name='remove_from_cart'),
    path('add_to_cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('<int:product_id>', views.product_details, name='product_details'),
    path('', views.homepage, name='homepage')
]
