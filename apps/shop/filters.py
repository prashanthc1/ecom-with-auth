import django_filters
from django import forms
from django_filters import CharFilter

from .models import Product, Tag


class ProductFilter(django_filters.FilterSet):
    headline = CharFilter(field_name="name", lookup_expr="icontains", label="name")
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Product
        fields = ["name", "tags"]
