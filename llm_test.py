import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("BLUESMINDS_API_KEY"),
    base_url="https://api.bluesminds.com/v1"
)


def generate_customer_response(order_analysis, policy):

    prompt = f"""
You are an AI Operations Assistant.

Generate a short and professional customer-facing response
based ONLY on the Order Analysis and Company Policy provided below.

Company Policy:
{policy}

Order Analysis:
{order_analysis}

Rules:
- Follow the company policy exactly.
- Do not invent information.
- Do not offer compensation that is not allowed by the policy.
- Do not add actions or requirements that are not mentioned in the policy.
- Keep the response clear, polite, and professional.
"""

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


policy = """
An order is officially classified as Delayed when the current date
exceeds the expected_delivery date and the shipment has not reached
Delivered status.

If delay is 1–3 days:
Notify the customer with an updated ETA. No compensation required.

If delay is 4–7 days:
Offer the customer a shipping fee refund or a 10% discount on the order.

If delay exceeds 7 days:
Offer a full shipping refund and escalate the shipment to Carrier Relations.

If delay exceeds 14 days:
Customer is eligible to cancel the order for a full refund.

Before responding to a delayed order inquiry:
Identify the delay reason recorded by the carrier.
Determine the applicable compensation tier based on days delayed.
"""


order_analysis = {
    "order_id": "ORD-4582",
    "status": "Delayed",
    "days_delayed": 6,
    "delay_reason": "Carrier warehouse congestion + incorrect address on first attempt",
    "recommended_action": "Offer shipping fee refund or 10% discount."
}


result = generate_customer_response(order_analysis, policy)

print(result)