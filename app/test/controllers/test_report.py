import pytest

from app.controllers import ReportController, OrderController

def test_report_failure(app):
    report, error = ReportController.get_report()
    pytest.assume(error is None)
    pytest.assume(report.get('best_customers') == [])
    pytest.assume(report.get('most_requested_ingredient') == [])
    pytest.assume(report.get('date_with_most_revenue') == [])

def test_get_report(create_order_mock):
    _, error_order = OrderController.create(create_order_mock)
    report, error = ReportController.get_report()
    pytest.assume(error is None)
    pytest.assume(error_order is None)
    pytest.assume(report.get('best_customers') != [])
    pytest.assume(report.get('best_customers') != [])
    pytest.assume(report.get('best_customers') != [])