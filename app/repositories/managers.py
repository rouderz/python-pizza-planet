from typing import Any, List, Optional, Sequence
import calendar
from sqlalchemy.sql import text, column, func, desc

from .models import OrderBeverage, Ingredient, Order, OrderDetail, Size, Beverage, db
from .serializers import (
    IngredientSerializer,
    OrderSerializer,
    SizeSerializer,
    BeverageSerializer,
    ma,
)


class BaseManager:
    model: Optional[db.Model] = None
    serializer: Optional[ma.SQLAlchemyAutoSchema] = None
    session = db.session

    @classmethod
    def get_all(cls):
        serializer = cls.serializer(many=True)
        _objects = cls.model.query.all()
        result = serializer.dump(_objects)
        return result

    @classmethod
    def get_by_id(cls, _id: Any):
        entry = cls.model.query.get(_id)
        return cls.serializer().dump(entry)

    @classmethod
    def create(cls, entry: dict):
        serializer = cls.serializer()
        new_entry = serializer.load(entry)
        cls.session.add(new_entry)
        cls.session.commit()
        return serializer.dump(new_entry)

    @classmethod
    def update(cls, _id: Any, new_values: dict):
        cls.session.query(cls.model).filter_by(_id=_id).update(new_values)
        cls.session.commit()
        return cls.get_by_id(_id)


class SizeManager(BaseManager):
    model = Size
    serializer = SizeSerializer


class IngredientManager(BaseManager):
    model = Ingredient
    serializer = IngredientSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        serializer = cls.serializer(many=True)
        _objects = cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []
        result = serializer.dump(_objects)
        return result

class OrderManager(BaseManager):
    model = Order
    serializer = OrderSerializer

    @classmethod
    def create(
        cls, order_data: dict, ingredients: List[Ingredient], beverages: List[Beverage]
    ):
        new_order = cls.model(**order_data)
        cls.session.add(new_order)
        cls.session.flush()
        cls.session.refresh(new_order)
        cls.session.add_all(
            (
                OrderDetail(
                    order_id=new_order._id,
                    ingredient_id=ingredient.get('_id'),
                    ingredient_price=ingredient.get('price'),
                )
                for ingredient in ingredients
            )
        )
        cls.session.add_all(
            OrderBeverage(
                order_id=new_order._id,
                beverage_id=beverage.get('_id'),
                beverage_price=beverage.get('_id'),
            )
            for beverage in beverages
        )
        cls.session.commit()
        return cls.serializer().dump(new_order)

    @classmethod
    def update(cls):
        raise NotImplementedError(f"Method not suported for {cls.__name__}")


class IndexManager(BaseManager):
    @classmethod
    def test_connection(cls):
        cls.session.query(column("1")).from_statement(text("SELECT 1")).all()


class BeverageManager(BaseManager):
    model = Beverage
    serializer = BeverageSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        serializer = cls.serializer(many=True)
        _objects = cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []
        result = serializer.dump(_objects)
        return result


class ReportManager(BaseManager):

    @classmethod
    def get_all_report(cls):
        return {
            'best_customers': cls.get_top_3_customers(),
            'most_requested_ingredient': cls.get_most_request_ingredients(),
            'date_with_most_revenue': cls.get_month_with_most_revenue()
        }

    @classmethod
    def get_top_3_customers(cls):
        customers = []
        data = cls.session.query(
            Order.client_name,
            func.sum(Order.total_price).label('total')
        ).group_by(Order.client_name).order_by(desc('total')).limit(3)
        if data is not None:
            for item in data:
                customers.append({
                    "client": item.client_name,
                    "total": round(item.total, 2)
                })
        return customers
        
    @classmethod
    def get_most_request_ingredients(cls) -> list:
        most_request_ingredients = []
        data = cls.session.query(
            Ingredient.name,
            func.count(OrderDetail.ingredient_id).label('times')
        ).join(OrderDetail).group_by(Ingredient).order_by(desc('times')).limit(3)
        
        if data is not None:
            for item in data:
                most_request_ingredients.append({
                "ingredient": item.name,
                "quantity": item.times
            })

        return most_request_ingredients

    
    @classmethod
    def get_month_with_most_revenue(cls):
        month = []
        data = cls.session.query(
            Order.date,
            func.sum(Order.total_price).label('total')
            ).group_by(Order.date).order_by(desc('total')).first()

        if data is not None:
            month.append({
                "month": data.date,
                "total_sales": round(data.total, 2)
            })

        return month
