from django import forms
from django.contrib.auth.models import Group

from shopapp.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = 'name',


class GroupCreateForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = "name",
