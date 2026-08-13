import pandas as pd
from docx import Document
from tools.operations_tools import (
    get_order_details,
    get_shipment_details,
    get_compensation,analyze_order
)

customers = pd.read_csv("data/customers.csv")
orders = pd.read_csv("data/orders.csv")
shipments = pd.read_csv("data/shipments.csv")


result = get_order_details("ORD-4582")
print(result)
    
result = get_shipment_details("ORD-4582")
print(result)

result = get_compensation(6)
print(result)

result = analyze_order("ORD-4582")
print(result)


doc = Document("data/Shipping_policy.docx")
policy_text = "\n".join(
    paragraph.text
    for paragraph in doc.paragraphs
    if paragraph.text.strip()
)
#print("\nSHIPPING POLICY:")
#print(policy_text)
def search_shipping_policy(keyword):
    results=[]
    for paragraph in policy_text.split("\n"):
        if keyword.lower() in paragraph.lower():
            results.append(paragraph)

    return results

result = search_shipping_policy("delay")
#print("\nPolicy Search:")
#print(result)

def check_order_delay(order_id):
    shipment =shipments[shipments["order_id"]== order_id]

    if shipment.empty:
        return "shipment not found"

    shipment = shipment.iloc[0]

    if shipment["current_status"]== "Delivered":
        return "order is not delayed"

    if shipment["days_delayed"] > 0:
        return f"order is delayed by{shipment['days_delayed']} days"
    return "order is not delayed"

result = check_order_delay("ORD-4582")
#print("\nDELAY CHECK:")
#print(result)



#print("\nRECOMMENDED ACTION:")
#print(action)


#result = analyze_order("ORD-4582")
#print("\nORDER ANALYSIS:")
#print(result)