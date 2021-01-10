from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from cart.cart import Cart
from shop.models import Product
from .forms import CartAddProductForm

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST or None)
    if form.is_valid():
        cd = form.cleaned_data
        quantity = cd['quantity']
        override_quantity = cd['override']
        cart.add(product, quantity, override_quantity)
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity' : item['quantity'],
            'override' : True
        })
    context = {
        'cart': cart
    }
    return render(request, 'cart/detail.html', context)