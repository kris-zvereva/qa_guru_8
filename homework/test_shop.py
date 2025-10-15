"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)

@pytest.fixture
def product2():
    return Product("pencil", 10, "This is a pencil", 500)

@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        assert product.check_quantity(999), f'Should return True: 999 <= {product.quantity}'
        assert product.check_quantity(1000), f'Should return True: 1000 <= {product.quantity}'
        assert not product.check_quantity(1001), f'Should return False: 1001 > {product.quantity}'

    def test_product_buy_less_than_available(self, product):
        product.buy(999)
        assert product.quantity == 1

    def test_product_buy_exact_amount(self, product):
        product.buy(1000)
        assert product.quantity == 0

    def test_product_buy_more_than_available(self, product):
        with pytest.raises(ValueError) as e:
            product.buy(product.quantity+1)
        assert str(e.value) == f'not enough product. quantity left: {product.quantity}'

class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """
    #add_product
    def test_add_new_product(self, product, cart):
        cart.add_product(product)

        assert product in cart.products
        assert cart.products[product] == 1

    def test_add_existing_product(self, product, cart):
        cart.add_product(product)
        cart.add_product(product)
        assert cart.products[product] == 2

    def test_add_product_with_custom_count(self, product, cart):
        cart.add_product(product, buy_count=4)
        assert cart.products[product] == 4

    def test_add_negative_product(self, product, cart):
        buy_count = -4
        with pytest.raises(ValueError) as e:
            cart.add_product(product, buy_count=buy_count)
        assert str(e.value) == f'Invalid buy_count: {buy_count}. Must be positive'

    #remove_product
    def test_remove_whole_product(self, product, cart):
        cart.add_product(product, buy_count=4)
        assert cart.products[product] == 4
        cart.remove_product(product)
        assert product not in cart.products

    def test_remove_some_product(self, product, cart):
        cart.add_product(product, buy_count=4)
        assert cart.products[product] == 4
        cart.remove_product(product, remove_count=2)
        assert product in cart.products
        assert cart.products[product] == 2

    def test_remove_more_of_product(self, product, cart):
        cart.add_product(product, buy_count=4)
        assert cart.products[product] == 4
        cart.remove_product(product, remove_count=5)
        assert product not in cart.products

    def test_remove_nonexistent_product(self, product, product2, cart):
        cart.add_product(product)
        assert cart.products[product] == 1
        with pytest.raises(KeyError):
            cart.remove_product(product2)

    #clear
    def test_cart_cleared(self, product, cart):
        cart.add_product(product, buy_count=4)
        cart.clear()
        assert cart.products == {}

    def test_empty_cart_cleared(self, cart):
        cart.clear()
        assert cart.products == {}

    #get_total_price
    def test_get_total_price(self, product, cart):
        cart.add_product(product, buy_count=4)
        expected_total = product.price * 4
        actual_total = cart.get_total_price()
        assert expected_total == actual_total

    def test_get_total_price_empty_cart(self, cart):
        assert cart.get_total_price() == 0

    def test_get_total_price_many_products(self, product, product2, cart):
        cart.add_product(product, buy_count=4)
        cart.add_product(product2, buy_count=5)
        expected_total = product.price * 4 + product2.price * 5
        actual_total = cart.get_total_price()
        assert expected_total == actual_total

    #buy
    def test_buy_cart(self, product, product2, cart):
        cart.add_product(product, buy_count=10)
        cart.add_product(product2, buy_count=100)
        assert product.quantity == 1000
        assert product2.quantity == 500

        cart.buy()

        assert product.quantity == 990
        assert product2.quantity == 400
        assert cart.products == {}

    def test_buy_cart_with_more_than_available(self, product, cart):
        attempted_buy_count = 1001
        cart.add_product(product, buy_count=attempted_buy_count)
        with pytest.raises(ValueError) as e:
            cart.buy()
        assert str(e.value) == f'Not enough of product {product.name} in quantity {attempted_buy_count} in the warehouse'
        assert product.quantity == 1000


    def test_buy_empty_cart(self, cart):
        cart.buy()
        assert cart.products == {}