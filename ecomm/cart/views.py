from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from django.shortcuts import render
from .cart import Cart
from .models import Order, OrderItem
from .forms import CheckoutForm
import razorpay
from django.conf import settings

def view_cart(request):
    cart = Cart(request)
    cart_items = cart.get_items()
    total_price = cart.get_total_price()
    context = {'cart_items': cart_items, 'total_price': total_price}
    return render(request, 'cart/view_cart.html', context)


def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product.id)
    return redirect('cart:view_cart')


def remove_from_cart(request, item_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=item_id)
    cart.remove(product.id)
    return redirect('cart:view_cart')


def update_cart(request, item_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=item_id)
    quantity = int(request.POST.get('quantity'))
    if quantity > 0:
        cart.add(product.id, quantity=quantity)
    else:
        cart.remove(product.id)
    return redirect('cart:view_cart')


def checkout(request):
    cart = Cart(request)
    cart_items = cart.get_items()
    total_price = cart.get_total_price()
    form = CheckoutForm()

    if request.method == 'POST':

        form = CheckoutForm(request.POST)
        if form.is_valid():
            billing_name = form.cleaned_data['billing_name']
            billing_email = form.cleaned_data['billing_email']
            billing_address = form.cleaned_data['billing_address']
            billing_phone = form.cleaned_data['billing_phone']
            shipping_name = form.cleaned_data['shipping_name']
            shipping_address = form.cleaned_data['shipping_address']
            card_number = form.cleaned_data['card_number']
            card_expiry = form.cleaned_data['card_expiry']
            card_cvv = form.cleaned_data['card_cvv']

            order = Order.objects.create(
                billing_name=billing_name,
                billing_email=billing_email,
                billing_address=billing_address,
                billing_phone=billing_phone,
                shipping_name=shipping_name,
                shipping_address=shipping_address,
                card_number=card_number,
                card_expiry=card_expiry,
                card_cvv=card_cvv
            )

            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity
                )

            cart_items.delete()
            cart.update_total_price()

            # Create payment using Razorpay API
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            amount = int(total_price) * 100
            order_currency = 'INR'
            order_receipt = str(order.id)


            payment = client.order.create(amount=amount, currency=order_currency, receipt=order_receipt)

            razor_pay_order_id = payment.get('id')

            context = {
                'order': order,
                'total_price': total_price,
                'razor_pay_order_id': razor_pay_order_id,
                'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            }

            return render(request, 'cart/checkout.html', context)


    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form,
    }

    return render(request, 'cart/checkout.html', context)

def order_confirmation(request):
    return render(request, 'order_confirmation.html')
