from django.shortcuts import render
from django.views import View
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


class OrderCreateView(View):
    def get(self, request):
        cart = Cart(request)
        form = OrderCreateForm()
        return render(request, "orders/order/create.html", {"cart": cart, "form": form})

    def post(self, request):
        cart = Cart(request)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item["product"],
                                         price=item["price"],
                                         quantity=item["quantity"])
            cart.clear()
            return render(request, "orders/order/created.html", {"order": order})
        return render(request, "orders/order/create.html", {"cart": cart, "form": form})
