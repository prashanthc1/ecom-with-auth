from django.urls import path

from .views import cartitems, checkout, contact, detail, home, index, shop, updateItem

app_name = "shop"

urlpatterns = [
    path("", home, name="home"),
    path("contact/", contact, name="contact"),
    path("cart/", cartitems, name="cart"),
    path("checkout/", checkout, name="checkout"),
    path("index/", index, name="index"),
    path("shop/", shop, name="shop"),
    path("detail/<str:id>/", detail, name="detail"),
    path("update-item/", updateItem, name="updateItem"),
]
