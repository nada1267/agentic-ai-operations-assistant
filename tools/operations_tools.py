import pandas as pd

from rag.retriever import retrieve


customers = pd.read_csv("data/customers.csv")
orders = pd.read_csv("data/orders.csv")
shipments = pd.read_csv("data/shipments.csv")


def get_order_details(order_id):
    order = orders[orders["order_id"] == order_id]

    if order.empty:
        return "Order not found"

    customer_id = order.iloc[0]["customer_id"]
    customer = customers[customers["customer_id"] == customer_id]

    shipment = shipments[shipments["order_id"] == order_id]

    return {
        "order": order.to_dict("records")[0],
        "customer": customer.to_dict("records")[0],
        "shipment": shipment.to_dict("records")[0]
    }


def get_shipment_details(order_id):
    shipment = shipments[shipments["order_id"] == order_id]

    if shipment.empty:
        return "Shipment not found"

    return shipment.to_dict("records")[0]


def get_compensation(days_delayed):
    if days_delayed <= 3:
        return "Notify customer with updated ETA. No compensation required."

    elif days_delayed <= 7:
        return "Offer shipping fee refund or 10% discount."

    elif days_delayed <= 14:
        return "Offer full shipping refund and escalate to Carrier Relations."

    else:
        return "Offer full refund and allow customer to cancel the order."


def analyze_order(order_id):
    shipment = shipments[shipments["order_id"] == order_id]

    if shipment.empty:
        return "Shipment not found"

    shipment = shipment.iloc[0]

    status = shipment["current_status"]

    # Delivered orders are not delayed
    if status == "Delivered":
        return {
            "order_id": order_id,
            "status": status,
            "days_delayed": 0,
            "delay_reason": shipment["delay_reason"],
            "recommended_action": "No action required. Order has been delivered."
        }

    # Returned orders are not treated as delayed
    if status == "Returned":
        return {
            "order_id": order_id,
            "status": status,
            "days_delayed": 0,
            "delay_reason": shipment["delay_reason"],
            "recommended_action": "Order was returned. Do not apply delay compensation."
        }

    # Processing orders are not treated as delayed
    if status == "Processing":
        return {
            "order_id": order_id,
            "status": status,
            "days_delayed": 0,
            "delay_reason": shipment["delay_reason"],
            "recommended_action": "Order is still being processed. No delay compensation."
        }

    # In Transit orders with 0 delay are not delayed
    if status == "In Transit" and shipment["days_delayed"] == 0:
        return {
            "order_id": order_id,
            "status": status,
            "days_delayed": 0,
            "delay_reason": shipment["delay_reason"],
            "recommended_action": "Order is in transit and is not currently delayed."
        }

    # Delayed orders
    if status == "Delayed":
        days_delayed = int(shipment["days_delayed"])

        action = get_compensation(days_delayed)

        return {
            "order_id": order_id,
            "status": status,
            "days_delayed": days_delayed,
            "delay_reason": shipment["delay_reason"],
            "recommended_action": action
        }

    # Unknown status
    return {
        "order_id": order_id,
        "status": status,
        "days_delayed": 0,
        "delay_reason": shipment["delay_reason"],
        "recommended_action": "No compensation decision can be made for this shipment status."
    }

def retrieve_policy(query):
    results = retrieve(query, top_k=3)

    documents = results["documents"][0]

    return "\n\n".join(documents)