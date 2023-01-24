import pytest

from app.test.utils.functions import get_random_price, get_random_string

def test_create_orders_service(create_orders):
    for value in create_orders:
        pytest.assume(value.json["_id"])
        pytest.assume(value.json["client_name"])
        pytest.assume(value.json["client_phone"])
        pytest.assume(value.json["client_dni"])
        pytest.assume(value.json["client_name"])
        pytest.assume(value.status.startswith('200'))

def test_create_order_service(create_order):
    order = create_order.json
    pytest.assume(order["_id"])
    pytest.assume(order["client_name"])
    pytest.assume(order["client_phone"])
    pytest.assume(order["client_dni"])
    pytest.assume(order["client_name"])
    pytest.assume(order["detail"])
    pytest.assume(order["size"])
    pytest.assume(create_order.status.startswith('200'))

def get_order_by_id_service(create_order, client, order_uri):
    order = create_order.json
    response = client.get(f'{order_uri}id/{order["_id"]}')
    pytest.assume(response.status.startswith('200'))
    returned_order = response.json
    for param, value in order.items():
        pytest.assume(returned_order[param] == value)
    
def get_all_orders_service(create_order, client, order_uri):
    response = client.get(order_uri)
    pytest.assume(response.status.startswith("200"))
    returned_order = {order_data["_id"]: order_data for order_data in response.json}
    for order in create_order:
        pytest.assume(order["_id"] in returned_order)



