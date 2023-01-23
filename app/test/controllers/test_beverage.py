import pytest
from app.controllers import BeverageController


def test_create(app, beverage: dict):
    create, error = BeverageController.create(beverage)
    pytest.assume(error is None)
    for param, value in beverage.items():
        pytest.assume(param in create)
        pytest.assume(value == create[param])
        pytest.assume(create["_id"])


def test_update(app, beverage: dict):
    create, _ = BeverageController.create(beverage)
    update_beverage_fields = {"name": "Coca-Cola", "price": 20}
    updated, error = BeverageController.update(
        {"_id": create["_id"], **update_beverage_fields}
    )
    pytest.assume(error is None)
    for param, value in update_beverage_fields.items():
        pytest.assume(update_beverage_fields[param] == value)


def test_get_by_id(app, beverage: dict):
    create, _ = BeverageController.create(beverage)
    beverage_from_db, error = BeverageController.get_by_id(create["_id"])
    pytest.assume(error is None)
    for param, value in create.items():
        pytest.assume(beverage_from_db[param] == value)


def test_get_all_beverages(app, beverages: list):
    created_beverages = []
    for beverage in beverages:
        created_beverage, _ = BeverageController.create(beverage)
        created_beverages.append(created_beverage)

    beverage_from_db, error = BeverageController.get_all()
    search_beverages = {
        beverage_db["_id"]: beverage_db for beverage_db in beverage_from_db
    }
    pytest.assume(error is None)
    for created_beverage in created_beverages:
        _id = created_beverage["_id"]
        assert _id in search_beverages
        for param, value in created_beverage.items():
            pytest.assume(search_beverages[_id][param] == value)
