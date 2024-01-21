from django.http import HttpResponse
from django.shortcuts import redirect, render
from cart.models import UserCart

from shop.models import Product,Order


# Create your views here.
def cart_page(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    cart_items = UserCart.objects.filter(user_id=request.user.id,in_cart=True)

    total =0
    for i in cart_items:
        total=total+i.product.price        
    print(cart_items,total)
    context = {
        'cart_items': cart_items,
        'total':total
    }
    return render(request, 'cart/cart.html',context)


def checkout(request):

    if not request.user.is_authenticated:
        return redirect('/')
   
    cart_items = UserCart.objects.filter(user_id=request.user.id,in_cart=True)
    total =0
    orderdetails = ''
    for i in cart_items:
        total=total+i.product.price 
        orderdetails = i.product.name + ' , '      
    print(cart_items,total)

    if request.method == 'POST':
        print(request.POST)
        delivery_address = request.POST['address']+" - "+request.POST['mobile']
        order = Order.objects.create(user_id=request.user.id,amount=total,delivery_address=delivery_address,details=orderdetails)
        print(order)
        UserCart.objects.filter(user_id=request.user.id,in_cart=True).update(in_cart=False)
        return redirect('/cart/order_placed?message=your order has been placed successfuly,pls pay INR {0} to our delivery boy. Thank you'.format(total))

    context = {
        'cart_items': cart_items,
        'total':total
    }    
    return render(request, 'cart/checkout.html',context)

def order_placed(request):
    if not request.user.is_authenticated :
        return redirect('/')
    print(request.GET)
    if not request.GET['message'] :
        return redirect('/')
    return render(request, 'cart/thankyou.html',{'msg':request.GET['message']})


def add_product_to_cart(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if request.method == 'GET':
        val=request.GET['id']
        item = Product.objects.get(pk=val)
        usercart = UserCart.objects.create(user=request.user,product=item,in_cart=True)
        return redirect("/cart")

    else:
        HttpResponse('only post method allowed')

def remove_product_from_cart(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if request.method == 'GET':
        val=request.GET['id']
        print(val)
        usercart = UserCart.objects.get(id=int(val))
        usercart.delete()
        return redirect("/cart")

    else:
        HttpResponse('only post method allowed')
