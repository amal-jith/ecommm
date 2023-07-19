
from django.urls import path
from .import views


app_name = 'store'

urlpatterns = [
    path('', views.category_product_list, name='category_product_list'),
    path('category/<slug:category_slug>', views.category_product_list, name='category_product_list_by_category'),
    path('product/<slug:product_slug>', views.product_detail, name='product_detail'),

]
