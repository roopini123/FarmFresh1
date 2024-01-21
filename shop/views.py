from django.shortcuts import render
from .models import Category, Product


def shop_page(request):
    category = Category.objects.all()
    products = Product.objects.filter(is_draft=False,is_stock_avaialable=True)

    if "cid" in request.GET and request.GET['cid']:
        products= products.filter(category_id=int(request.GET['cid']))
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'shop/shop.html', context)


def product_details(request, product_id):
    product_details = Product.objects.get(id=product_id)
    ctg = Category.objects.get(name=product_details.category)
    related_products = Product.objects.filter(category=ctg)
    context = {
        'product': product_details,
        'related_products': related_products
    }
    return render(request, 'shop/product-details.html', context)


def wishlist(request):
    return render(request, 'shop/wishlist.html')

