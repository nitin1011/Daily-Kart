from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Products
from django.contrib.auth.decorators import login_required
from accounts.models import Account
import os
from django.contrib.auth.models import User

# Create your views here.


# fetch all the products from the table

# Home page
def home(request):
    product_all = Products.objects.all()

    context = {'product1': product_all[0], 'product2': product_all[1], 'product3': product_all[2],
               'product4': product_all[3], 'product5': product_all[4], 'product6': product_all[5]}

    return render(request, 'products/home.html', context)

#About page
def about(request):
    return render(request, 'products/about.html')


def privacy(request):
    return render(request, 'products/privacy.html')


def terms(request):
    return render(request, 'products/terms.html')

def product_detail(request, pk):
    product = Products.objects.get(pk=pk)
    if request.method == 'POST':
        # path = os.path.realpath(product.product_image)
        # os.remove(path)
        product.product_image = request.FILES['image']
        product.save()
    context = {'object': product}
    try:
        account = Account.objects.get(user=request.user)
        if account.category == 'shopkeeper' and product.user == request.user:
            context['shop'] = True
    except:
        context['shop'] = False
    return render(request, 'products/products_detail.html', context)


def edit_product(request, pk):
    product = Products.objects.get(pk=pk)
    context = {'product': product}
    if request.method == 'POST':
        product.product_name = request.POST['name']
        product.product_category = request.POST['category']
        product.product_price = request.POST['price']
        product.product_discount = request.POST['discount']
        product.product_disc = request.POST['discription']
        product.save()
        return redirect('product-detail', product.id)
    else:
        return render(request, 'products/edit_product.html', context)

def delete_product(request, pk):
    product = Products.objects.get(pk=pk)
    product.delete()
    return redirect('home')

@login_required
def add_product(request):
    account = Account.objects.get(user=request.user)
    if account.category == 'shopkeeper':
        if request.method == 'POST':
            name = request.POST['productname']
            category = request.POST['productcategory']
            price = request.POST['productprice']
            discount = request.POST['discount']
            image = request.FILES['image']
            disc = request.POST['discription']

            product = Products(user=request.user, product_name=name, product_category=category, product_price=price,
                               product_discount=discount, product_image=image, product_disc=disc)
            product.save()
            return redirect('product-detail', product.id)
        else:
            return render(request, 'products/products_form.html')
    else:
        messages.error(request, "You are not shopkeeper")
        return redirect('login')


@login_required
def all_product(request):
    account = Account.objects.get(user=request.user)
    if account.category == 'shopkeeper':
        user = request.user
        context = {'products': user.products_set.all()}
        return render(request, 'products/all_products.html', context)
    else:
        return redirect('home')
