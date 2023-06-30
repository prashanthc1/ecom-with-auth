from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

from .filters import ProductFilter
from .models import Category, Customer, Order, Product


def home(request):
    products = Product.objects.all()
    myFilter = ProductFilter(request.GET, queryset=products)
    products = myFilter.qs
    page = request.GET.get("page")
    paginator = Paginator(products, 6)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {"products": products, "myFilter": myFilter}
    # products = Product.objects.all()
    # context = {"products": products}
    print("hello world")
    return render(request, "shop/home.html", context)


def cartitems(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {
            "get_cart_total": 0,
            "get_cart_items": 0,
            "get_cart_total_with_shipping": 0,
        }
    context = {"items": items, "order": order}
    return render(request, "shop/cart.html", context)


def contact(request):
    print("hello world")
    return render(request, "shop/contact.html")


def checkout(request):
    return render(request, "shop/checkout.html")


def index(request):
    return render(request, "shop/index.html")


def shop(request):
    return render(request, "shop/shop.html")


def detail(request, id):
    product = Product.objects.get(id=id)
    context = {"product": product}
    return render(request, "shop/detail.html", context)


def cart(request):
    return render(request, "shop/cart.html")
