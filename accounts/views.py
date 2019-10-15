from django.contrib import messages, auth
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Account
# Create your views here.


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        mobile = request.POST['mobile']
        state = request.POST['state']
        city = request.POST['city']
        area = request.POST['area']
        address = request.POST['address']
        password = request.POST['password']
        password2 = request.POST['password2']
        category = request.POST['category']
        if 'terms' in request.POST:
            if password == password2:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'That username is taken')
                    return redirect('register')
                else:
                    if User.objects.filter(email=email).exists():
                        messages.error(request, 'That email is already being used ')
                        return redirect('register')
                    else:
                        if len(mobile) != 10:
                            messages.error(request, 'Mobile no. is incorrect')
                            return redirect('register')
                        else:
                            user = User.objects.create_user(username=username, password=password, email=email,
                                                            first_name=firstname, last_name=lastname)

                            user.save()
                            account = Account(user=user, username=username, firstname=firstname, lastname=lastname,
                                              email=email, mobile=mobile, state=state, city=city, area=area, address=address,
                                              category=category)
                            if category == 'delivery':
                                account.shop = request.POST['shop']
                            account.save()
                            messages.success(request, "Your account has been created successfully")
                            return redirect('login')
            else:
                messages.error(request, 'Password do not match')
                return redirect('register')
        else:
            messages.error(request, 'you have to accept the Terms and Conditions')
            return  redirect('register')
    else:
        accounts = Account.objects.filter(category='shopkeeper')
        context = {'shop1': accounts[0], 'shops': accounts[1:]}
        return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        category = request.POST['category']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            account = Account.objects.get(user=user)
            if account.category == category:
                auth.login(request, user)
                return redirect('account')
            else:
                s = "you are not " + str(category)
                messages.error(request, s)
                return redirect('login')
        else:
            messages.error(request, 'Username/Password is incorrect')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required
def user_account(request):
    account = Account.objects.get(user=request.user)
    context = {'account': account}
    if account.category == 'shopkeeper':
        shop = True
        context['shop'] = shop
    elif account.category == 'delivery':
        delivery = True
        context['delivery'] = delivery
    return render(request, 'accounts/user_account.html', context)

@login_required
def edit_account(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        mobile = request.POST['mobile']
        state = request.POST['state']
        city = request.POST['city']
        area = request.POST['area']
        address = request.POST['address']
        account = Account.objects.get(user=request.user)
        if User.objects.filter(email=email).exists() and account.email != email:
            messages.error(request, 'That email is already being used ')
            return redirect('edit-account')
        else:
            if Account.objects.filter(mobile=mobile).exists() and account.mobile != mobile:
                messages.error(request, 'That mobile is already being used ')
                return redirect('edit-account')
            else:
                account.firstname = firstname
                account.lastname = lastname
                account.email = email
                account.mobile = mobile
                account.state = state
                account.city = city
                account.area = area
                account.address = address
                account.save()
                return redirect('account')
    else:
        account = Account.objects.get(user=request.user)
        context = {'account': account}
        return render(request, 'accounts/edit_account.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        password = request.POST['old']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        user = auth.authenticate(username=request.user.username, password=password)
        if user == request.user:
            if password1 == password2:
                user.set_password(password1)
                user.save()
                return redirect('login')
            else:
                return redirect('change-password')
        else:
            messages.error(request, 'Wrong password')
            return redirect('change-password')
    else:
        return render(request, 'accounts/change_password.html')

@login_required
def delete_account(request):
    user = request.user
    user.delete()
    return redirect('home')
