from django.shortcuts import render, redirect , get_object_or_404
from django.views import View
from home.models import Product
from .cart import Cart



class CartView(View):
    def get(self, request):
        return render(request, "orders/cart.html")


class CartAddView(View):
    def post(self, request, product_id):
        pass
