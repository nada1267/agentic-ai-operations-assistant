import sys
sys.path.append(".")
from tools.operations_tools import (
    get_order_details,
    get_shipment_details,
    get_compensation,
    analyze_order
)


# ==========================================
# 1. Order Not Found
# ==========================================

def test_get_order_not_found():

    result = get_order_details("ORD-9999")

    assert result == "Order not found"


# ==========================================
# 2. Compensation: 1-3 Days
# ==========================================

def test_compensation_1_to_3_days():

    result = get_compensation(3)

    assert "No compensation required" in result


# ==========================================
# 3. Compensation: 4-7 Days
# ==========================================

def test_compensation_4_to_7_days():

    result = get_compensation(7)

    assert "shipping fee refund" in result
    assert "10% discount" in result


# ==========================================
# 4. Compensation: More Than 7 Days
# ==========================================

def test_compensation_more_than_7_days():

    result = get_compensation(10)

    assert "full shipping refund" in result
    assert "Carrier Relations" in result


# ==========================================
# 5. Compensation: More Than 14 Days
# ==========================================

def test_compensation_more_than_14_days():

    result = get_compensation(15)

    assert "full refund" in result
    assert "cancel" in result


# ==========================================
# 6. In Transit
# ==========================================

def test_analyze_in_transit():

    result = analyze_order("ORD-4601")

    assert result["status"] == "In Transit"
    assert result["days_delayed"] == 0
    assert "not currently delayed" in result["recommended_action"]


# ==========================================
# 7. Processing
# ==========================================

def test_analyze_processing():

    result = analyze_order("ORD-4587")

    assert result["status"] == "Processing"
    assert result["days_delayed"] == 0
    assert "No delay compensation" in result["recommended_action"]


# ==========================================
# 8. Returned
# ==========================================

def test_analyze_returned():

    result = analyze_order("ORD-4611")

    assert result["status"] == "Returned"
    assert result["days_delayed"] == 0
    assert "Do not apply delay compensation" in result["recommended_action"]


# ==========================================
# 9. Delivered
# ==========================================

def test_analyze_delivered():

    result = analyze_order("ORD-4575")

    assert result["status"] == "Delivered"
    assert result["days_delayed"] == 0
    assert "No action required" in result["recommended_action"]


# ==========================================
# 10. Delayed 4-7 Days
# ==========================================

def test_analyze_delayed_4_to_7():

    result = analyze_order("ORD-4590")

    assert result["status"] == "Delayed"
    assert result["days_delayed"] == 7
    assert "shipping fee refund" in result["recommended_action"]
    assert "10% discount" in result["recommended_action"]


# ==========================================
# 11. Delayed More Than 7 Days
# ==========================================

def test_analyze_delayed_more_than_7():

    result = analyze_order("ORD-4581")

    assert result["status"] == "Delayed"
    assert result["days_delayed"] > 7
    assert "full refund" in result["recommended_action"]
    assert "cancel" in result["recommended_action"]


# ==========================================
# 12. Delayed More Than 14 Days
# ==========================================

def test_analyze_delayed_more_than_14():

    result = analyze_order("ORD-4582")

    assert result["status"] == "Delayed"
    assert result["days_delayed"] > 14
    assert "full refund" in result["recommended_action"]