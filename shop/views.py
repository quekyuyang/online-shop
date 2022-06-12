from django.shortcuts import render
from .models import Product, ProductImage, Category
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ProductForm, AddToCartForm, LoginForm, ReviewForm
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib import auth
from django.db.models import Avg
from .cart import Cart


def homepage(request):
    products = Product.objects.all()
    categories = Category.objects.filter(parent__isnull=True)
    template = loader.get_template('shop/browse.html')
    context = {'products': products, 'sibling_categories': categories}
    return HttpResponse(template.render(context, request))


def add_product(request):
    if request.method == 'GET':
        form = ProductForm(label_suffix='')
    elif request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, label_suffix='')
        if form.is_valid() and len(request.FILES.getlist('images')) <= 5:
            product = form.save(commit=False)
            product.seller = request.user
            product_images = []
            product.save()
            product.categories.add(*form.cleaned_data['categories'])
            for imagefile in request.FILES.getlist('images'):
                product_image = ProductImage(product=product, image=imagefile)
                product_images.append(product_image)
                product_image.save()
            product.primary_image = product_images[form.cleaned_data['i_primary_image']]
            product.save()
            return HttpResponseRedirect(reverse(homepage))
    template = loader.get_template('shop/add_product.html')
    context = {'form':form}
    return HttpResponse(template.render(context, request))


def product_details(request, product_id):
    product = Product.objects.get(id=product_id)
    add_to_cart_form = AddToCartForm()
    review_form = ReviewForm(label_suffix='')
    review_form['content'].label = 'Leave a Review'
    reviews = product.review_set.all()
    mean_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    recent_reviews = reviews.reverse()[:5]

    template = loader.get_template('shop/product_details.html')
    context = {'product': product, 'add_to_cart_form': add_to_cart_form,
               'review_form': review_form, 'reviews': recent_reviews,
               'mean_rating': mean_rating}
    return HttpResponse(template.render(context, request))


@require_POST
def post_review(request, product_id):
    product = Product.objects.get(id=product_id)
    review_form = ReviewForm(request.POST, label_suffix='')
    if review_form.is_valid():
        review = review_form.save(commit=False)
        review.product = product
        review.user = request.user
        review.save()

    return HttpResponseRedirect(reverse('product_details', args=[product_id]))


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


def browse(request, category_name):
    category = Category.objects.get(name=category_name)

    if category.parent:
        sibling_categories = category.parent.children
    else:
        sibling_categories = Category.objects.filter(parent__isnull=True)
    sibling_categories = sibling_categories.exclude(id=category.id)

    child_categories = category.children.all()

    products = category_products(category)
    template = loader.get_template('shop/browse.html')
    context = {
        'products': products,
        'current_category': category,
        'sibling_categories': sibling_categories,
        'child_categories': child_categories,
        'parent_category': category.parent
        }
    return HttpResponse(template.render(context, request))


def category_products(category):
    products = category.product_set.all()
    if products:
        return products
    else:
        child_categories = category.children.all()
        products = Product.objects.none()
        for child_category in child_categories:
            products = products.union(category_products(child_category))
        return products
