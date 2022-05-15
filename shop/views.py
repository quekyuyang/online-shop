from django.shortcuts import render
from .models import Product, ProductImage
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ProductForm, AddToCartForm
from django.urls import reverse
from django.views.decorators.http import require_POST
from .cart import Cart


def homepage(request):
    products = Product.objects.all()
    template = loader.get_template('shop/homepage.html')
    context = {'products': products}
    return HttpResponse(template.render(context, request))


def add_product(request):
    if request.method == 'GET':
        form = ProductForm()
    elif request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product_images = []
            product.save()
            for imagefile in request.FILES.getlist('images'):
                product_image = ProductImage(product=product, image=imagefile)
                product_images.append(product_image)
                product_image.save()
            product.primary_image = product_images[0]
            product.save()
            return HttpResponseRedirect(reverse(homepage))

    template = loader.get_template('shop/add_product.html')
    context = {'form':form}
    return HttpResponse(template.render(context, request))


def product_details(request, product_id):
    product = Product.objects.get(id=product_id)
    add_to_cart_form = AddToCartForm()
    template = loader.get_template('shop/product_details.html')
    context = {'product': product, 'add_to_cart_form': add_to_cart_form}
    return HttpResponse(template.render(context, request))


@require_POST
def add_to_cart(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    form = AddToCartForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add_product(product_id, cd['quantity'])
    return HttpResponseRedirect(reverse(homepage))
