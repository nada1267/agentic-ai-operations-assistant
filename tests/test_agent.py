import sys
sys.path.append(".")

from agent import run_agent


# ==========================================
# 1. Order Not Found
# ==========================================

def test_order_not_found():

    result = run_agent("ORD-9999")

    assert result == "Order not found"


# ==========================================
# 2. Delayed Order + RAG Policy
# ==========================================
def test_delayed_order_with_policy():

    result = run_agent(
        "What compensation is available for order ORD-4590?"
    ).lower()

    assert (
        "shipping fee refund" in result
        or "refund of the shipping fee" in result
    )

    assert "10%" in result

# ==========================================
# 3. Normal Order Status
# ==========================================

def test_processing_order():

    result = run_agent(
        "What is the status of order ORD-4587?"
    ).lower()

    assert "processing" in result