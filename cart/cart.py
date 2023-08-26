from django.conf import settings
from decimal import Decimal
from shop.models import Product
from typing import Dict, Union, Any


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart: Dict[str, Union[Dict[str, Union[int, str]], Any]] = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product: Product, quantity: int = 1, override_quantity: bool = False) -> None:
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0,
                                     "price": str(product.price)}
        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += 1
        self.save()

    def save(self) -> None:
        self.session.modified = True

    def remove(self, product: Product) -> None:
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"] = product
        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self) -> int:
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self) -> Decimal:
        return sum(Decimal(item["price"]) * item["quantity"]
                   for item in self.cart.values())

    def clear(self) -> None:
        del self.session[settings.CART_SESSION_ID]
        self.save()
