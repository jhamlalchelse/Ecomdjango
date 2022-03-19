from itertools import product
from django import dispatch
from django.shortcuts import redirect, render
from django.views import View
from app.forms import CustomerProfileForm, CustomerRegistrationForms
from app.models import Customer, ProductDetail, Cart, ProductPlaced
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# def home(request):
#  return render(request, 'app/home.html')
class ProductView(View):
    def get(self, request):
        topwears = ProductDetail.objects.filter(category='TW')
        bottomwears = ProductDetail.objects.filter(category='BW')
        mobiles = ProductDetail.objects.filter(category='M')
        laptops = ProductDetail.objects.filter(category='L')
        data = {
            'topwears': topwears,
            'bottomwears': bottomwears,
            'mobiles': mobiles,
            'laptops': laptops,
        }
        return render(request, 'app/home.html', data)
# def product_detail(request):
#  return render(request, 'app/productdetail.html')
class ProductDetailView(View):
    def get(self, request, pk):
        product = ProductDetail.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {'product': product,'item_already_in_cart':item_already_in_cart})

@login_required(login_url='../account/login')
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = ProductDetail.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

@login_required(login_url='../account/login')
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount=0.0
        shipping_amount=70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==user]
        if cart_product:
            for c in cart_product:
                amount += c.product.discount_price*c.quantity
            total_amount = amount + shipping_amount
            data={
                'carts':cart,
                'amount':amount,
                'shipping_amount':shipping_amount,
                'total_amount':total_amount,
            }
            return render(request, 'app/addtocart.html',data)
        else:
            return render(request, 'app/nocartitem.html')
            
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity = c.quantity + 1
        totalquantity = c.quantity
        print(c.quantity)
        c.save()
        amount=0.0
        shipping_amount=70.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for cp in cart_product:
            amount += cp.product.discount_price*cp.quantity
        total_amount = amount + shipping_amount
        data={
            'quantity': totalquantity,
            'amount': amount,
            'total_amount': total_amount,
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity = c.quantity - 1
        totalquantity = c.quantity
        print(c.quantity)
        c.save()
        amount=0.0
        shipping_amount=70.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for cp in cart_product:
            amount += cp.product.discount_price*cp.quantity
        total_amount = amount + shipping_amount
        print(totalquantity)
        data={
            'quantity': totalquantity,
            'amount': amount,
            'total_amount': total_amount,
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount=0.0
        shipping_amount=70.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for cp in cart_product:
            amount += cp.product.discount_price*cp.quantity
        total_amount = amount + shipping_amount
        data={
            'amount': amount,
            'total_amount': total_amount,
        }
        return JsonResponse(data)


def buy_now(request):
    return render(request, 'app/buynow.html')

# def profile(request):
#     return render(request, 'app/profile.html')

@login_required(login_url='../account/login')
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

@login_required(login_url='../account/login')
def orders(request):
    user = request.user
    order_placed = ProductPlaced.objects.filter(user=user)
    print(order_placed)
    return render(request, 'app/orders.html',{'order_placed':order_placed})

def mobile(request, data = None):
    if data == None:
        mobiles = ProductDetail.objects.filter(category='M')
    elif data=='Redmi':
        mobiles = ProductDetail.objects.filter(category='M').filter(brand=data)
    elif data=='Realme':
        mobiles = ProductDetail.objects.filter(category='M').filter(brand=data)
    elif data=='Oneplus':
        mobiles = ProductDetail.objects.filter(category='M').filter(brand=data)
    elif data=='Samsung':
        mobiles = ProductDetail.objects.filter(category='M').filter(brand=data)
    elif data=='Below':
        mobiles = ProductDetail.objects.filter(category='M').filter(discount_price__lt=20000)
    elif data=='Range':
        mobiles = ProductDetail.objects.filter(category='M').filter(discount_price__gte=20000, discount_price__lte=30000)
    elif data=='Above':
        mobiles = ProductDetail.objects.filter(category='M').filter(discount_price__gt=30000)
    datavalue=data
    return render(request, 'app/mobile.html', {'mobiles':mobiles,'datavalue':datavalue})
def laptop(request, data = None):
    if data == None:
        laptop = ProductDetail.objects.filter(category='L')
    elif data=='mac':
        laptop = ProductDetail.objects.filter(category='L').filter(brand=data)
    elif data=='lenovo':
        laptop = ProductDetail.objects.filter(category='L').filter(brand=data)
    elif data=='hp':
        laptop = ProductDetail.objects.filter(category='L').filter(brand=data)
    elif data=='predator':
        laptop = ProductDetail.objects.filter(category='L').filter(brand=data)
    elif data=='Below':
        laptop = ProductDetail.objects.filter(category='L').filter(discount_price__lt=50000)
    elif data=='Range':
        laptop = ProductDetail.objects.filter(category='L').filter(discount_price__gte=50000, discount_price__lte=100000)
    elif data=='Above':
        laptop = ProductDetail.objects.filter(category='L').filter(discount_price__gt=100000)
    datavalue=data
    return render(request, 'app/laptop.html', {'laptops':laptop,'datavalue':datavalue})

def topwear(request, data = None):
    if data == None:
        topwear = ProductDetail.objects.filter(category='TW')
    elif data=='denim':
        topwear = ProductDetail.objects.filter(category='TW').filter(brand=data)
    elif data=='zara':
        topwear = ProductDetail.objects.filter(category='TW').filter(brand=data)
    elif data=='Below':
        topwear = ProductDetail.objects.filter(category='TW').filter(discount_price__lt=1000)
    elif data=='Range':
        topwear = ProductDetail.objects.filter(category='TW').filter(discount_price__gte=1000, discount_price__lte=3000)
    elif data=='Above':
        topwear = ProductDetail.objects.filter(category='TW').filter(discount_price__gt=3000)
    datavalue=data
    return render(request, 'app/topwear.html', {'topwears':topwear,'datavalue':datavalue})

def bottomwear(request, data = None):
    if data == None:
        bottomwear = ProductDetail.objects.filter(category='BW')
    elif data=='denim':
        bottomwear= ProductDetail.objects.filter(category='BW').filter(brand=data)
    elif data=='roadstar':
        bottomwear= ProductDetail.objects.filter(category='BW').filter(brand=data)
    elif data=='Below':
        bottomwear = ProductDetail.objects.filter(category='BW').filter(discount_price__lt=1000)
    elif data=='Range':
        bottomwear = ProductDetail.objects.filter(category='BW').filter(discount_price__gte=1000, discount_price__lte=2000)
    elif data=='Above':
        bottomwear = ProductDetail.objects.filter(category='BW').filter(discount_price__gt=2000)
    datavalue=data
    return render(request, 'app/bottomwear.html', {'bottomwears':bottomwear,'datavalue':datavalue})


def login(request):
    return render(request, 'app/login.html')

# def customerregistration(request):
#     return render(request, 'app/customerregistration.html')
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForms()
        return render(request, 'app/customerregistration.html',{'form':form})
    def post(self,request):
        form = CustomerRegistrationForms(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulation!! Registration Successfully')
            form.save()
        return render(request, 'app/customerregistration.html',{'form':form})

@login_required(login_url='../account/login')  
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_item= Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=70.0
    total_amount = 0.0 
    cart_product = [p for p in Cart.objects.all() if p.user==request.user]
    if cart_product:
        for cp in cart_product:
            amount += cp.product.discount_price*cp.quantity
        total_amount = amount + shipping_amount
    return render(request, 'app/checkout.html',{'add':add,'total_amount':total_amount,'cart_product':cart_product})

@method_decorator(login_required(login_url='../account/login'), name='dispatch')
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html',{'form':form,'active':'btn-primary'})

    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
        messages.success(request,'Congratulation !! Profile Update Successfully')
        return render(request, 'app/profile.html',{'form':form,'active':'btn-primary'})

@login_required(login_url='../account/login')
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        ProductPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('orders')
