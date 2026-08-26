import pandas as pd

from tools.operations_tools import (
    get_order_details,
    get_shipment_details,
    get_compensation,
    analyze_order,
    retrieve_policy
)


# ==========================================
# Load Data
# ==========================================

customers = pd.read_csv("data/customers.csv")
orders = pd.read_csv("data/orders.csv")
shipments = pd.read_csv("data/shipments.csv")


# ==========================================
# Test 1: Get Order Details
# ==========================================

print("\n" + "=" * 50)
print("TEST 1: Get Order Details")
print("=" * 50)

result = get_order_details("ORD-4582")
print(result)


# ==========================================
# Test 2: Get Shipment Details
# ==========================================

print("\n" + "=" * 50)
print("TEST 2: Get Shipment Details")
print("=" * 50)

result = get_shipment_details("ORD-4582")
print(result)


# ==========================================
# Test 3: Compensation - 2 Days Delay
# ==========================================

print("\n" + "=" * 50)
print("TEST 3: Compensation - 2 Days")
print("=" * 50)

result = get_compensation(2)
print(result)


# ==========================================
# Test 4: Compensation - 6 Days Delay
# ==========================================

print("\n" + "=" * 50)
print("TEST 4: Compensation - 6 Days")
print("=" * 50)

result = get_compensation(6)
print(result)


# ==========================================
# Test 5: Compensation - 10 Days Delay
# ==========================================

print("\n" + "=" * 50)
print("TEST 5: Compensation - 10 Days")
print("=" * 50)

result = get_compensation(10)
print(result)


# ==========================================
# Test 6: Compensation - 15 Days Delay
# ==========================================

print("\n" + "=" * 50)
print("TEST 6: Compensation - 15 Days")
print("=" * 50)

result = get_compensation(15)
print(result)


# ==========================================
# Test 7: Analyze Existing Order
# ==========================================

print("\n" + "=" * 50)
print("TEST 7: Analyze ORD-4582")
print("=" * 50)

result = analyze_order("ORD-4582")
print(result)


# ==========================================
# Test 8: Non-existing Order
# ==========================================

print("\n" + "=" * 50)
print("TEST 8: Non-existing Order")
print("=" * 50)

result = get_order_details("ORD-9999")
print(result)


# ==========================================
# Test 9: Non-existing Shipment
# ==========================================

print("\n" + "=" * 50)
print("TEST 9: Non-existing Shipment")
print("=" * 50)

result = get_shipment_details("ORD-9999")
print(result)


# ==========================================
# Test 10: Analyze Non-existing Order
# ==========================================

print("\n" + "=" * 50)
print("TEST 10: Analyze Non-existing Order")
print("=" * 50)

result = analyze_order("ORD-9999")
print(result)


# ==========================================
# Test 11: Retrieve Policy Using RAG
# ==========================================

print("\n" + "=" * 50)
print("TEST 11: Retrieve Shipping Policy")
print("=" * 50)

result = retrieve_policy(
    "compensation for an order delayed 5 days"
)

print(result)


# ==========================================
# Test 12: Analyze Existing Order + Policy
# ==========================================

print("\n" + "=" * 50)
print("TEST 12: Full Delay Analysis")
print("=" * 50)

order_result = get_order_details("ORD-4582")
analysis_result = analyze_order("ORD-4582")

print("\nOrder:")
print(order_result)

print("\nAnalysis:")
print(analysis_result)

print("\nPolicy:")
print(
    retrieve_policy(
        "compensation for delayed orders"
    )
)

