from django.shortcuts import render , get_object_or_404
from django.views import View
from .models import Product


class HomeView(View):
    def get(self, request):
        return render(request, "home/home.html")


class ProductsView(View):
    def get(self , request):
        products = Product.objects.all()
        return render(request ,"home/products.html",{'products':products})
    

class ProductDetailView(View):
    def get(self , request , slug):
        product = get_object_or_404(Product , slug = slug)
        return render(request ,"home/product_detail.html",{'product':product})