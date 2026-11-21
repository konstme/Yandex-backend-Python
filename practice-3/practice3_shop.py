from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP


def money(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


@dataclass(eq=False)
class Product:
    name: str
    price: Decimal
    stock: int
    category: str

    def __post_init__(self) -> None:
        if self.price < 0 or self.stock < 0:
            raise ValueError("Цена и запас не могут быть отрицательными")


@dataclass
class Order:
    customer_name: str
    items: list[tuple[Product, int, Decimal]]
    discount: Decimal
    tax: Decimal

    @property
    def subtotal(self) -> Decimal:
        return money(sum((price * qty for _, qty, price in self.items), Decimal("0")))

    @property
    def total(self) -> Decimal:
        return money(self.subtotal * (1 - self.discount) * (1 + self.tax))


@dataclass
class Customer:
    name: str
    email: str
    order_history: list[Order] = field(default_factory=list)


@dataclass
class ShoppingCart:
    items: dict[Product, int] = field(default_factory=dict)

    def update_quantity(self, product: Product, quantity: int) -> None:
        if quantity < 0:
            raise ValueError("Количество не может быть отрицательным")
        if quantity > product.stock:
            raise ValueError(f"Недостаточно товара: {product.name}")
        if quantity == 0:
            self.items.pop(product, None)
        else:
            self.items[product] = quantity

    def add(self, product: Product, quantity: int = 1) -> None:
        if quantity <= 0:
            raise ValueError("Добавляемое количество должно быть положительным")
        self.update_quantity(product, self.items.get(product, 0) + quantity)

    def remove(self, product: Product) -> None:
        self.items.pop(product, None)

    def checkout(self, customer: Customer, discount: Decimal = Decimal("0"),
                 tax: Decimal = Decimal("0")) -> Order:
        if not self.items:
            raise ValueError("Корзина пуста")
        if not (0 <= discount <= 1) or tax < 0:
            raise ValueError("Скидка должна быть от 0 до 1, налог — неотрицательным")
        for product, quantity in self.items.items():
            if quantity > product.stock:
                raise ValueError(f"Недостаточно товара: {product.name}")
        order = Order(customer.name,
                      [(product, qty, product.price) for product, qty in self.items.items()],
                      discount, tax)
        for product, quantity in self.items.items():
            product.stock -= quantity
        customer.order_history.append(order)
        self.items.clear()
        return order


if __name__ == "__main__":
    laptop = Product("Ноутбук", Decimal("50000"), 3, "Электроника")
    mouse = Product("Мышь", Decimal("1000"), 10, "Аксессуары")
    customer = Customer("Анна", "anna@example.com")
    cart = ShoppingCart()
    cart.add(laptop)
    cart.add(mouse, 2)
    cart.update_quantity(mouse, 3)
    order = cart.checkout(customer, discount=Decimal("0.10"), tax=Decimal("0.20"))
    print(f"Покупатель: {order.customer_name}")
    print(f"До скидки: {order.subtotal} ₽; итог: {order.total} ₽")
    print(f"Заказов в истории: {len(customer.order_history)}; мышей на складе: {mouse.stock}")
