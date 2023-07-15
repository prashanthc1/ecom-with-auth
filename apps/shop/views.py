import json

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.shortcuts import render

from .filters import ProductFilter
from .models import Category, Order, OrderItem, Product


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

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        items = []
        order = {
            "get_cart_total": 0,
            "get_cart_items": 0,
            "get_cart_total_with_shipping": 0,
        }
        cartitems = order["get_cart_items"]

    categories = Category.objects.all()
    context = {
        "products": products,
        "myFilter": myFilter,
        "order": order,
        "items": items,
        "cartitems": cartitems,
        "categories": categories,
    }
    # products = Product.objects.all()
    # context = {"products": products}
    return render(request, "shop/home.html", context)


def cartitems(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        items = []
        order = {
            "get_cart_total": 0,
            "get_cart_items": 0,
            "get_cart_total_with_shipping": 0,
        }
        cartitems = order["get_cart_items"]
    context = {
        "items": items,
        "order": order,
        "cartitems": cartitems,
    }
    return render(request, "shop/cart.html", context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        items = []
        order = {
            "get_cart_total": 0,
            "get_cart_items": 0,
            "get_cart_total_with_shipping": 0,
        }
        cartitems = order["get_cart_items"]
    context = {
        "items": items,
        "order": order,
        "cartitems": cartitems,
    }
    return render(request, "shop/checkout.html", context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]
    # print("action: ", action)
    # print("id: ", productId)

    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, completed=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        orderItem.quantity = orderItem.quantity + 1
    elif action == "remove":
        orderItem.quantity = orderItem.quantity - 1
    elif action == "delete":
        orderItem.quantity = 0

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    # print(action)
    return JsonResponse("item was added successfully", safe=False)


def contact(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        items = []
        order = {
            "get_cart_total": 0,
            "get_cart_items": 0,
            "get_cart_total_with_shipping": 0,
        }
        cartitems = order["get_cart_items"]
    context = {
        "items": items,
        "order": order,
        "cartitems": cartitems,
    }
    return render(request, "shop/contact.html", context)


def detail(request, id):
    product = Product.objects.get(id=id)
    context = {"product": product}
    return render(request, "shop/detail.html", context)


def index(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        items = []
        order = {
            "get_cart_total": 0,
            "get_cart_items": 0,
            "get_cart_total_with_shipping": 0,
        }
        cartitems = order["get_cart_items"]
    context = {
        "items": items,
        "order": order,
        "cartitems": cartitems,
    }
    return render(request, "shop/index.html", context)


def shop(request):
    return render(request, "shop/shop.html")
