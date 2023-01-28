from flask_seeder import Faker, generator, Seeder
from faker import Faker as faker
from random import randint, choice
from datetime import datetime
from app.seeds.data import ingredients, beverages, sizes, clients
from app.repositories.models import (
    Order,
    Beverage,
    Ingredient,
    Size,
    OrderDetail,
    OrderBeverage,
)
from app.plugins import db
from app.controllers import *


def create_items(model, data) -> list:
    return [model(name=key, price=value) for key, value in data.items()]


def create_orders(count: int, clients) -> list:
    new_order = []
    order_detail = []
    beverage_detail = []
    fake = faker()
    ingredients, _ = IngredientController.get_all()
    sizes, _ = SizeController.get_all()
    beverages, _ = BeverageController.get_all()
    for index in range(1, count + 1):
        size = sizes[randint(0, len(sizes) - 1)]
        ingredient = ingredients[randint(0, len(ingredients) - 1)]
        beverage = beverages[randint(0, len(beverages) - 1)]
        name = clients[randint(0, len(clients) - 1)]
        
        new_order.append(
            Order(
                client_name=name,
                client_dni=fake.pyint(99999999, 999999999),
                client_phone=fake.pyint(99999999, 999999999),
                client_address=fake.address(),
                total_price=OrderController.calculate_order_price(
                    size["price"], ingredients, beverages
                ),
                date=fake.date_between(datetime.fromisoformat('2020-01-01'), datetime.fromisoformat(datetime.now().date().isoformat())),
                size_id=size["_id"],
            )
        )

        order_detail.append(
            OrderDetail(
                order_id=index,
                ingredient_price=ingredient["price"],
                ingredient_id=ingredient["_id"],
            )
        )

        beverage_detail.append(
            OrderBeverage(
                order_id=index,
                beverage_price=beverage["price"],
                beverage_id=beverage["_id"],
            )
        )

    return new_order, order_detail, beverage_detail


class DatabaseSeeder(Seeder):
    @classmethod
    def run(self):
        ingredient = create_items(Ingredient, ingredients)
        size = create_items(Size, sizes)
        beverage = create_items(Beverage, beverages)
        self.insert_db(ingredient)
        self.insert_db(size)
        self.insert_db(beverage)

        order, order_detail, beverage_detail = create_orders(100, clients)
        self.insert_db(order)
        self.insert_db(order_detail)
        self.insert_db(beverage_detail)

    def insert_db(data):
        for item in data:
            db.session.add(item)
