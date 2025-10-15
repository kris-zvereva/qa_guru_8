import logging

logger = logging.getLogger(__name__)


class Product:
    """
    Класс продукта
    """
    name: str
    price: float
    description: str
    quantity: int

    def __init__(self, name, price, description, quantity):
        self.name = name
        self.price = price
        self.description = description
        self.quantity = quantity

    def check_quantity(self, quantity) -> bool:
        """
        TODO Верните True если количество продукта больше или равно запрашиваемому
            и False в обратном случае
        """
        return self.quantity >= quantity

    def buy(self, quantity):
        """
        TODO реализуйте метод покупки
            Проверьте количество продукта используя метод check_quantity
            Если продуктов не хватает, то выбросите исключение ValueError
        """
        if self.check_quantity(quantity):
            self.quantity -= quantity
            logger.info(f'product is bought. quantity left : {self.quantity}')
        else:
            raise ValueError(f'not enough product. quantity left: {self.quantity}')

    def __hash__(self):
        return hash(self.name + self.description)


class Cart:
    """
    Класс корзины. В нем хранятся продукты, которые пользователь хочет купить.
    TODO реализуйте все методы класса
    """

    # Словарь продуктов и их количество в корзине
    products: dict[Product, int]

    def __init__(self):
        # По-умолчанию корзина пустая
        self.products = {}

    def add_product(self, product: Product, buy_count=1):
        """
        Метод добавления продукта в корзину.
        Если продукт уже есть в корзине, то увеличиваем количество
        """
        if buy_count <= 0:
            raise ValueError(f'Invalid buy_count: {buy_count}. Must be positive')
        if product in self.products:
            self.products[product] += buy_count
            logger.info(f'Product {product.name} count increased to {self.products[product]}')
        else:
            self.products[product] = buy_count
            logger.info(f'Product {product.name} added to cart. Count: {buy_count}')

    def remove_product(self, product: Product, remove_count=None):
        """
        Метод удаления продукта из корзины.
        Если remove_count не передан, то удаляется вся позиция
        Если remove_count больше, чем количество продуктов в позиции, то удаляется вся позиция
        """
        if remove_count is None or remove_count >= self.products[product]:
            self.products.pop(product)
            logger.info(f'Product {product.name} removed from cart')
        else:
            self.products[product] -= remove_count
            logger.info(f'Product {product.name} count decreased to {self.products[product]}')

    def clear(self):
        self.products.clear()
        logger.info('Cart cleared')

    def get_total_price(self) -> float:
        total = 0.0
        for product, quantity in self.products.items():
            total += product.price * quantity
        return total

    def buy(self):
        """
        Метод покупки.
        Учтите, что товаров может не хватать на складе.
        В этом случае нужно выбросить исключение ValueError
        """
        for product, quantity in self.products.items():
            if not product.check_quantity(quantity):
                raise ValueError(f'Not enough of product {product.name} in quantity {quantity} in the warehouse')

        for product, quantity in self.products.items():
            product.buy(quantity)
        self.clear()
