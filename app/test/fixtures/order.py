import pytest

from ..utils.functions import (shuffle_list, get_random_sequence,
                               get_random_string)



@pytest.fixture
def order_uri():
    return '/order/'


@pytest.fixture
def client_data() -> dict:
    return {
        'client_address': get_random_string(),
        'client_dni': get_random_sequence(),
        'client_name': get_random_string(),
        'client_phone': get_random_sequence()
    }


@pytest.fixture
def create_order_mock(create_ingredients, create_sizes, client_data) -> dict:
    ingredients = [ingredient.get("_id") for ingredient in create_ingredients]
    sizes = [size.get('_id') for size in create_sizes]
    return {
        **client_data,
        'ingredients': ingredients,
        'size_id': shuffle_list(sizes)[0]
    }

@pytest.fixture
def create_order(client, order_uri, create_order_mock) -> dict:
    response = client.post(order_uri, json=create_order_mock)
    return response


@pytest.fixture
def create_orders(client, order_uri, create_ingredients, create_sizes, client_data) -> list:
    ingredients = [ingredient.get('_id') for ingredient in create_ingredients]
    sizes = [size.get('_id') for size in create_sizes]
    orders = []
    for _ in range(10):
        new_order = client.post(order_uri, json={
            **client_data,
            'ingredients': shuffle_list(ingredients)[:5],
            'size_id': shuffle_list(sizes)[0]
        })
        orders.append(new_order)
    return orders
