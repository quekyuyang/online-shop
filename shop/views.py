from django.shortcuts import render
from .models import Product, ProductImage
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ProductForm
from django.urls import reverse


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
    template = loader.get_template('shop/product_details.html')
    context = {'product': product}
    return HttpResponse(template.render(context, request))
