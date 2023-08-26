from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product, quantity=cd["quantity"])
        return redirect("cart:cart_detail")


class CartRemoveView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect("cart:cart_detail")


class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)
        for item in cart:
            item["update_quantity_form"] = CartAddProductForm(initial={
                "quantity": item["quantity"],
                "override": True})
        return render(request, "cart/detail.html", {"cart": cart})
