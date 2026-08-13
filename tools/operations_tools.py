import pandas as pd

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

    if shipment["current_status"] == "Delivered":
        return "Order is already delivered."

    days_delayed = shipment["days_delayed"]

    action = get_compensation(days_delayed)

    return {
        "order_id": order_id,
        "status": shipment["current_status"],
        "days_delayed": days_delayed,
        "delay_reason": shipment["delay_reason"],
        "recommended_action": action
    }

def retrive_policy():
    with open("knowledge/company_policy.txt","r",encoding="utf-8") as file:
        policy=file.read()

        return policy

