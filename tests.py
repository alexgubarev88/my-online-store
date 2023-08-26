from django.test import TestCase, Client
from django.urls import reverse, resolve
from cart.views import CartDetailView, CartAddView, CartRemoveView
from cart.forms import CartAddProductForm
from orders.forms import OrderCreateForm
from orders.models import OrderItem, Order
from orders.views import OrderCreateView
from shop.models import Category, Product
from shop.views import ProductListView, ProductDetailView


class CategoryModelTest(TestCase):
    """Test the Category model."""

    def setUp(self):
        """Create a test Category instance."""
        self.category = Category.objects.create(name="Test Category", slug="test-category")

    def test_str_representation(self):
        """Test the string representation of the Category."""
        self.assertEqual(str(self.category), "Test Category")

    def test_get_absolute_url(self):
        """Test the get_absolute_url method of Category."""
        expected_url = reverse("shop:product_list_by_category", args=[self.category.slug])
        self.assertEqual(self.category.get_absolute_url(), expected_url)


class ProductModelTest(TestCase):
    """Test the Product model."""

    def setUp(self):
        """Create a test Product instance."""
        category = Category.objects.create(name="Test Category", slug="test-category")
        self.product = Product.objects.create(
            category=category,
            name="Test Product",
            slug="test-product",
            price=10.99,
        )

    def test_str_representation(self):
        """Test the string representation of the Product."""
        self.assertEqual(str(self.product), "Test Product")

    def test_get_absolute_url(self):
        """Test the get_absolute_url method of Product."""
        expected_url = reverse("shop:product_detail", args=[self.product.id, self.product.slug])
        self.assertEqual(self.product.get_absolute_url(), expected_url)


class CategoryViewsTest(TestCase):
    """Test views related to Category model."""

    def setUp(self):
        """Create a test Category instance."""
        self.category = Category.objects.create(name="Test Category", slug="test-category")

    def test_category_list_view(self):
        """Test the category_list view."""
        response = self.client.get(reverse("shop:product_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Category")

    def test_category_detail_view(self):
        """Test the category_detail view."""
        response = self.client.get(self.category.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Category")


class ProductViewsTest(TestCase):
    """Test views related to Product model."""

    def setUp(self):
        """Create a test Category instance."""
        category = Category.objects.create(name="Test Category", slug="test-category")
        self.product = Product.objects.create(
            category=category,
            name="Test Product",
            slug="test-product",
            price=10.99,
        )

    def test_product_list_view(self):
        """Test the product_list view."""
        response = self.client.get(reverse("shop:product_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")

    def test_product_detail_view(self):
        """Test the product_detail view."""
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")


class ShopUrlsTest(TestCase):
    """Test the URLs and their associated views in the "shop" app."""

    def setUp(self):
        """Create test Category and Product instances for URL testing."""
        self.category = Category.objects.create(name="Test Category", slug="test-category")
        self.product = Product.objects.create(
            category=self.category,
            name="Test Product",
            slug="test-product",
            price=10.99,
        )

    def test_product_list_url(self):
        """Test the URL for the product list view."""
        url = reverse("shop:product_list")
        self.assertEqual(resolve(url).func.view_class, ProductListView)

    def test_product_list_by_category_url(self):
        """Test the URL for the product list by category view."""
        url = reverse("shop:product_list_by_category", args=[self.category.slug])
        self.assertEqual(resolve(url).func.view_class, ProductListView)

    def test_product_detail_url(self):
        """Test the URL for the product detail view."""
        url = reverse("shop:product_detail", args=[self.product.id, self.product.slug])
        self.assertEqual(resolve(url).func.view_class, ProductDetailView)


class ProductListViewTest(TestCase):
    """Test the ProductListView view."""

    def setUp(self):
        """Create test Category and Product instances for testing."""
        self.client = Client()
        self.category = Category.objects.create(name="Test Category", slug="test-category")
        self.product = Product.objects.create(
            category=self.category,
            name="Test Product",
            slug="test-product",
            price=10.99,
            available=True,
        )

    def test_product_list_view_without_category(self):
        """Test the product list view without providing a category."""
        response = self.client.get(reverse("shop:product_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")

    def test_product_list_view_with_category(self):
        """Test the product list view with a specific category."""
        response = self.client.get(reverse("shop:product_list_by_category", args=[self.category.slug]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")
        self.assertContains(response, self.category.name)


class OrderModelTest(TestCase):
    """Test the Order model."""

    def setUp(self):
        """Create test Category, Product, Order, and OrderItem instances for testing."""
        self.category = Category.objects.create(name="Test Category", slug="test-category")
        self.product = Product.objects.create(
            category=self.category,
            name="Test Product",
            slug="test-product",
            price=10.99,
            available=True,
        )
        self.order = Order.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            address="123 Main St",
            postal_code="12345",
            city="New York",
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=10.99,
            quantity=2,
        )

    def test_order_str_representation(self):
        """Test the string representation of the Order."""
        self.assertEqual(str(self.order), f'Order {self.order.id}')

    def test_get_total_cost(self):
        """Test the get_total_cost method of the Order."""
        expected_total = self.order_item.get_cost()
        decimal_total = float(self.order.get_total_cost())
        decimal_total_rounded = round(decimal_total, 2)

        self.assertEqual(decimal_total_rounded, expected_total)


class OrderItemModelTest(TestCase):
    """Test the OrderItem model."""

    def setUp(self):
        """Create test Category, Product, Order, and OrderItem instances for testing."""
        self.category = Category.objects.create(name="Test Category", slug="test-category")
        self.product = Product.objects.create(
            category=self.category,
            name="Test Product",
            slug="test-product",
            price=10.99,
            available=True,
        )
        self.order = Order.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            address="123 Main St",
            postal_code="12345",
            city="New York",
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=10.99,
            quantity=2,
        )

    def test_order_item_str_representation(self):
        """Test the string representation of the OrderItem."""
        self.assertEqual(str(self.order_item), str(self.order_item.id))

    def test_get_cost(self):
        """Test the get_cost method of the OrderItem."""
        expected_cost = self.order_item.price * self.order_item.quantity
        self.assertEqual(self.order_item.get_cost(), expected_cost)


class OrderCreateFormTest(TestCase):
    """Test the OrderCreateForm form."""

    def test_form_valid_data(self):
        """Test the form with valid data."""
        form = OrderCreateForm(data={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "address": "123 Main St",
            "postal_code": "12345",
            "city": "New York",
        })

        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        """Test the form with invalid data."""
        form = OrderCreateForm(data={
            "first_name": "",
            "last_name": "Doe",
            "email": "john@example.com",
            "address": "123 Main St",
            "postal_code": "12345",
            "city": "New York",
        })

        self.assertFalse(form.is_valid())


class OrdersUrlsTest(TestCase):
    """Test the URLs and their associated views in the "orders" app."""

    def test_order_create_url(self):
        url = reverse("orders:order_create")
        self.assertEqual(resolve(url).func.view_class, OrderCreateView)


class CartAddProductFormTest(TestCase):
    """Test the CartAddProductForm form."""

    def test_form_valid_data(self):
        """Test the form with valid data."""
        form = CartAddProductForm(data={
            "quantity": 3,
            "override": False,
        })

        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        """Test the form with invalid data."""
        form = CartAddProductForm(data={
            "quantity": 25,
            "override": False,
        })

        self.assertFalse(form.is_valid())


class CartUrlsTest(TestCase):
    """Test the URLs and their associated views in the "cart" app."""

    def test_cart_detail_url(self):
        """Test the cart detail URL."""
        url = reverse("cart:cart_detail")
        self.assertEqual(resolve(url).func.view_class, CartDetailView)

    def test_cart_add_url(self):
        """Test the cart add URL."""
        url = reverse("cart:cart_add", args=[1])
        self.assertEqual(resolve(url).func.view_class, CartAddView)

    def test_cart_remove_url(self):
        """Test the cart remove URL."""
        url = reverse("cart:cart_remove", args=[1])
        self.assertEqual(resolve(url).func.view_class, CartRemoveView)


class CartAddViewTest(TestCase):
    """
    Test case for the CartAddView.
    """

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(name="Test Product", price=10.0, category=self.category)
        self.url = reverse("cart:cart_add", args=[self.product.id])

    def test_add_to_cart(self):
        """
        Test adding a product to the cart using CartAddView.
        """
        response = self.client.post(self.url, {"quantity": 2})
        self.assertEqual(response.status_code, 302)


class CartRemoveViewTest(TestCase):
    """
    Test case for the CartRemoveView.
    """

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(name="Test Product", price=10.0, category=self.category)
        self.url = reverse("cart:cart_remove", args=[self.product.id])

    def test_remove_from_cart(self):
        """
        Test removing a product from the cart using CartRemoveView.
        """
        self.client.session["cart"] = {"product_id": {"quantity": 1}}
        self.client.session.save()

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
