from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from Kart.models import Kart, CartItem
from accounts.models import Account
from .models import Order, History, HistoryItem
from .utils import id_generator
from datetime import datetime
# Create your views here.

@login_required
def order_list(request):
    account = Account.objects.get(user=request.user)
    if account.category == 'customer':
        orders = Order.objects.filter(user=request.user)
        if len(orders) == 0:
            context = {'empty': True}
        else:
            context = {'orders': orders, 'shopkeeper': False, 'other': False}
    elif account.category == 'shopkeeper':
        orders = Order.objects.filter(shop_user=request.user.username)
        if len(orders) == 0:
            context = {'empty': True}
        else:
            context = {'orders': orders, 'shopkeeper': True, 'other': False}
    elif account.category == 'delivery':
        orders = Order.objects.filter(delivery_boy=request.user.username)
        if len(orders) == 0:
            context = {'empty': True}
        else:
            context = {'orders': orders, 'other': False}
    else:
        context = {'other': True}
    return render(request, 'order/order_list.html', context)


@login_required
def order_detail(request, id):
    order = Order.objects.get(id=id)
    account = Account.objects.get(user=request.user)
    if account.category == 'customer':
        if order.status == 'Notstarted':
            kart = Kart.objects.get(user=request.user)
            shop_account = Account.objects.get(username=order.shop_user)
            context = {'products': kart.cartitem_set.all(), 'shopkeeper': False, 'order': order, 'other': False,
                       'accept': False, 'customer': True, 'shop_account': shop_account}
        else:
            history = History.objects.get(user=request.user)
            history_item = HistoryItem.objects.filter(history=history, order=order)
            shop_account = Account.objects.get(username=order.shop_user)
            context = {'products': history_item, 'shopkeeper': False, 'order': order, 'other': False, 'accept': True,
                       'shop_account': shop_account, 'customer': True}
            if order.status != 'Canceled':
                delivery_account = Account.objects.get(username=order.delivery_boy)
                context['delivery_account'] = delivery_account
            if order.status == 'Finished':
                context['finished'] = True
            if order.status == 'Canceled':
                context['canceled'] = True
    elif account.category == 'shopkeeper':
        if order.status == 'Notstarted':
            kart = Kart.objects.get(user=order.user)
            accounts = Account.objects.filter(category='delivery', shop=request.user.username)
            context = {'products': kart.cartitem_set.all(), 'shopkeeper': True, 'order': order, 'other': False,
                       'accept': False, 'delivery': accounts[0], 'deliveries': accounts[1:]}
        else:
            history = History.objects.get(user=order.user)
            history_item = HistoryItem.objects.filter(history=history, order=order)

            context = {'products': history_item, 'shopkeeper': True, 'order': order, 'other': False, 'accept': True}
            if order.status == 'Canceled':
                context['canceled'] = True
            if order.status == 'Finished':
                context['finished'] = True
    elif account.category == 'delivery':
        if order.status == 'Notstarted':
            kart = Kart.objects.get(user=order.user)
            context = {'products': kart.cartitem_set.all(), 'delivery_boy': True, 'other': False, 'accept': False, 'order': order, 'shopkeeper': False}
        else:
            history = History.objects.get(user=order.user)
            history_item = HistoryItem.objects.filter(history=history, order=order)
            context = {'products': history_item, 'delivery_boy': True, 'other': False, 'accept': True, 'order': order, 'shopkeeper': False}
            if order.status == 'Finished':
                context['finished'] = True
    else:
        context = {'other': True}
    return render(request, 'order/order_detail.html', context)


def accepted(request, id):
    order = Order.objects.get(id=id)
    if request.method == 'POST':
        delivery = request.POST['delivery']
        deliveryboy = request.POST['deliveryboy']
        order.delivery_charge = delivery
        order.delivery_boy = deliveryboy
        order.status = 'Started'
        order.final_total = float(delivery)+float(order.sub_total)
        order.save()
        cartitem = order.cartitem_set.all()
        for i in range(len(cartitem)):
            print(cartitem[i])
            cartitem[i].delete()
    return redirect('order-detail', order.id)


def finished(request, id):
    order = Order.objects.get(id=id)
    order.status = 'Finished'
    order.save()
    return redirect('order-detail', order.id)

def canceled(request, id):
    order = Order.objects.get(id=id)
    order.status = 'Canceled'
    order.save()
    return redirect('order-detail', id)


def delete_order(request, id):
    order = Order.objects.get(id=id)
    order.delete()
    return redirect('order-list')

@login_required
def checkout(request):
    kart = Kart.objects.get(user=request.user)
    cartitem = CartItem.objects.filter(kart=kart)
    product = []
    try:
        new_history = History.objects.get(user=request.user)
    except History.DoesNotExist:
        new_history = History(user=request.user)
        new_history.save()
    except:
        pass
    for i in range(len(cartitem)):
        product.append(cartitem[i].product.user)
        history_item = HistoryItem(history=new_history, product=cartitem[i].product, quantity=cartitem[i].quantity,
                                   line_total=cartitem[i].line_total)
        history_item.save()

    order = []
    prod = set(product)
    prod = list(prod)
    history_item = new_history.historyitem_set.all()
    for i in range(len(prod)):
        line_total = 0
        now = datetime.now()
        d = now.strftime("%Y-%m-%d %H:%M")
        order.append(Order(user=request.user, shop_user=prod[i].username, order_id=id_generator()))
        order[i].datetime = d
        order[i].save()
        for j in range(len(cartitem)):
            if cartitem[j].product.user == prod[i]:
                cartitem[j].order = order[i]
                line_total += cartitem[j].line_total
                cartitem[j].save()
                history_item[len(history_item)-j-1].order = order[i]
                history_item[len(history_item)-j-1].save()
        order[i].sub_total = kart.total
        order[i].save()
    order = Order.objects.filter(user=request.user)
    context = {'orders': order, 'shopkeeper': False, 'other': False}
    return render(request, 'order/order_list.html', context)


@login_required
def history_view(request):
    try:
        history = History.objects.get(user=request.user)
        context = {'empty': False, 'history_item': history.historyitem_set.all()}
    except:
        context = {'empty': True}

    return render(request, 'order/history.html', context)


