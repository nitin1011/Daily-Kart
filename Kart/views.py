from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Kart, CartItem
from products.models import Products
from accounts.models import Account
# Create your views here.


@login_required
def view_kart(request):
    account = Account.objects.get(user=request.user)
    if account.category != 'customer':
        st = 'You are ' + account.category + ". You cannot buy the product"
        messages.error(request, st)
        return redirect('login')
    try:
        new_kart = Kart.objects.get(user=request.user)
        # the_id = request.session['kart_id']
    except Kart.DoesNotExist:
        new_kart = Kart()
        new_kart.user = request.user
        # the_id = None
    except:
        new_kart = None
    if new_kart:
        # kart = Kart.objects.get(id=the_id)
        if new_kart.cartitem_set.count() == 0:
            context = {'empty': True, 'message': 'Your cart is empty'}
        else:
            context = {'kart': new_kart}
    else:
        context = {'empty': True, 'message': 'Your cart is empty'}
    return render(request, 'Kart/view_kart.html', context)


@login_required
def update_kart(request, id):
    account = Account.objects.get(user=request.user)
    if account.category != 'customer':
        st = 'You are ' + account.category + ". You cannot buy the product"
        messages.error(request, st)
        return redirect('product-detail', id)
    try:
        qty = request.GET.get('qty')
        if len(qty) == 0:
            qty = 1
        update_qty = True
    except:
        qty = None
        update_qty = False

    try:
        # the_id = request.session['kart_id']
        new_kart = Kart.objects.get(user=request.user)
    except:
        new_kart = Kart()
        new_kart.user = request.user
        new_kart.save()
        # request.session['kart_id'] = new_kart.id
        # the_id = new_kart.id
    # kart = Kart.objects.get(id=the_id)

    product = Products.objects.get(id=id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, kart=new_kart, product=product)
    if created:
        new_kart.item_count = new_kart.cartitem_set.count()
    if update_qty:
        if int(qty) == 0:
            cart_item.delete()
        elif int(qty) < 0:
            messages.error(request, "You can't add negative no. of quantity into the cart ")
            return redirect('product-detail', id)
        else:
            cart_item.quantity = qty
            price = cart_item.product.product_price-(cart_item.product.product_price*(cart_item.product.product_discount/100))
            cart_item.line_total = price*int(cart_item.quantity)
            cart_item.save()
    else:
        pass

    new_total = 0.00
    request.session['item_count'] = new_kart.cartitem_set.count()
    for i in new_kart.cartitem_set.all():
        sp = i.product.product_price - (i.product.product_price*(i.product.product_discount/100))
        line_total = float(sp) * i.quantity
        new_total += float(line_total)
    new_kart.total = new_total
    new_kart.save()
    return redirect('view-kart')
