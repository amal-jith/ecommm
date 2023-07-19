from django.shortcuts import render, get_object_or_404
from .models import Category, Product

# Create your views here.
def category_product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'store/category_product_list.html', {'category': category, 'categories': categories, 'products': products})




def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    return render(request, 'store/product_detail.html', {'product':product})


