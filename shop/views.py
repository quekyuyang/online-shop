from django.shortcuts import render
from .models import Product, ProductImage
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ProductForm, AddToCartForm, LoginForm
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib import auth
from .cart import Cart


def homepage(request):
    products = Product.objects.all()
    template = loader.get_template('shop/homepage.html')
    context = {'products': products}
    return HttpResponse(template.render(context, request))


def add_product(request):
    if request.method == 'GET':
        form = ProductForm(label_suffix='')
    elif request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, label_suffix='')
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
        cart.add(product_id, cd['quantity'])
    return HttpResponseRedirect(reverse(homepage))


@require_POST
def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return HttpResponseRedirect(reverse('cart'))


def cart(request):
    cart = Cart(request)
    template = loader.get_template('shop/cart.html')
    context = {'cart': cart, 'total_price': cart.total_price()}
    return HttpResponse(template.render(context, request))


def login_page(request):
    if request.method == 'GET':
        form = LoginForm()
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = auth.authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect(reverse(homepage))
            else:
                return HttpResponse('Invalid login')

    template = loader.get_template('shop/login.html')
    context = {'form': form}
    return HttpResponse(template.render(context, request))

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse(homepage))
