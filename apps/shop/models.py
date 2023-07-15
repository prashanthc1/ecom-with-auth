import uuid

from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from apps.common.models import TimeStampedUUIDModel
from apps.users.models import User

# from django.contrib.auth.models import User


class Tag(TimeStampedUUIDModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Category(MPTTModel):
    pkid = models.BigAutoField(primary_key=True, editable=False, null=False, unique=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=50)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    description = models.CharField(max_length=200)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class Product(TimeStampedUUIDModel):
    name = models.CharField(max_length=50, null=False, blank=False)
    catogary = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_("Category"))
    image = models.ImageField(upload_to="ProductImages")
    offer_price = models.DecimalField(max_digits=5, decimal_places=2)
    actual_price = models.DecimalField(max_digits=5, decimal_places=2)
    details = models.TextField()
    description = models.TextField()
    information = models.TextField()
    active = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag)
    slug = models.SlugField(null=True, blank=True)

    class Meta:
        ordering = ["-id"]

    def save(self, *args, **kwargs):
        if self.slug == None:
            slug = slugify(self.name)
            has_slug = Product.objects.filter(slug=slug).exists()
            count = 1
            while has_slug:
                count += 1
                slug = slugify(self.name) + "-" + str(count)
                has_slug = Product.objects.filter(slug=slug).exists()
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url


# class Customer(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
#     name = models.CharField(max_length=200, null=True, blank=True)
#     email = models.EmailField(max_length=200, null=True, blank=True)

#     def __str__(self):
#         return self.name


class Order(TimeStampedUUIDModel):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    completed = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return str(self.pkid)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_total_with_shipping(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        shipping_price = 10
        total += shipping_price
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    @property
    def get_total(self):
        total = self.product.offer_price * self.quantity
        return total

    def __str__(self):
        return str(self.id)


class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=10, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
