import sys
sys.path.append(".")

from agent import run_agent


def test_order_not_found():
    result = run_agent("ORD-9999")
    assert result == "Order not found"


def test_delayed_order():
    result = run_agent("ORD-4582")
    assert "shipping fee refund" in result.lower() or "10% discount" in result.lower()


def test_in_transit_order():
    result = run_agent("ORD-4581")
    assert "no compensation" in result.lower()