import pytest

from app.test.utils.functions import get_random_price, get_random_string

def test_create_order_service(create_order):
    order = create_order.json
    pytest.assume(order["_id"])
    pytest.assume(order["client_name"])
    pytest.assume(order["client_phone"])
    pytest.assume(order["client_dni"])
    pytest.assume(order["client_name"])
    pytest.assume(create_order.status.startswith('200'))

def test_get_order_by_id_service(client, create_order, order_uri):
    order = create_order.json
    response = client.get(f'{order_uri}id/{order["_id"]}')
    pytest.assume(response.status.startswith("200"))
    returned_order = response.json
    for param, value in order.items():
        pytest.assume(returned_order[param] == value)

def test_get_all_orders_service(client, create_orders, order_uri):
    response = client.get(order_uri)
    pytest.assume(response.status.startswith("200"))
    returned_order = {order["_id"]: order for order in response.json}
    for order in create_orders:
        pytest.assume(order["_id"] in returned_order)
