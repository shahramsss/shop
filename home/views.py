from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Product, Category
from orders.forms import CartAddForm


class HomeView(View):
    def get(self, request):
        return render(request, "home/home.html")


class ProductsView(View):
    def get(self, request, category_slug=None):
        products = Product.objects.all()
        categories = Category.objects.all()
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            products = Product.objects.filter(category=category)
        return render(
            request,
            "home/products.html",
            {"products": products, "categories": categories},
        )


class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        form = CartAddForm()
        return render(
            request, "home/product_detail.html", {"product": product, "form": form}
        )
