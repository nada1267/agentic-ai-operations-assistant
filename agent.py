import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from tools.operations_tools import(
    get_order_details,
    get_shipment_details,
    analyze_order,retrive_policy

)
load_dotenv()

client = OpenAI(
    api_key=os.getenv("BLUESMINDS_API_KEY"),
    base_url="https://api.bluesminds.com/v1"
)
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_order_details",
            "description": "Get order, customer, and shipment details using an order ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The order ID, for example ORD-4582"
                    }
                },
                "required": ["order_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_order",
            "description": "Analyze an order and determine its delay status and recommended compensation action using company policy.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The order ID, for example ORD-4582"
                    }
                },
                "required": ["order_id"]
            }
        }
    },
    {
    "type": "function",
    "function": {
        "name": "retrieve_policy",
        "description": "Retrieve the company policy for handling delayed orders.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}
]
    
def run_agent(order_id):

    prompt = f"""
You are an AI Operations Assistant.

The customer is asking about order {order_id}.

Use the available tools to retrieve all information you need.

After getting the required information, provide a short,
professional customer-facing response.

Rules:
- Do not invent information.
- Follow the company policy.
- Do not offer compensation unless allowed by the tools/policy.
- Do not claim that you contacted a carrier or performed an action
  unless a tool explicitly confirms that action was performed.
- Keep the response clear, polite, and professional.
- Do not claim that an action was performed or will be performed unless a tool explicitly supports that action.
- Do not ask the customer for information unless it is required by the tools or policy.
- Do not promise to perform, submit, process, apply, contact, or follow up on any action unless a tool explicitly confirms that the action is available and has been performed.
"""

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    while True:

        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=messages,
            tools=tools
        )

        message = response.choices[0].message

        # لو الـLLM خلص ومحتاج يكتب الرد النهائي
        if not message.tool_calls:
            return message.content

        # نضيف رسالة الـLLM اللي فيها طلب الـTool
        messages.append(message)

        # تنفيذ الـTools المطلوبة
        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            print("Tool:", tool_name)
            print("Arguments:", arguments)

            if tool_name == "get_order_details":
                result = get_order_details(**arguments)
                if result == "Order not found":
                    return result

            elif tool_name == "analyze_order":
                result = analyze_order(**arguments)
                if result == "Shipment not found":
                    return result

            elif tool_name == "get_shipment_details":
                result = get_shipment_details(**arguments)
            elif tool_name == "retrieve_policy":
                result = retrive_policy()

            else:
                result = "Unknown tool."

            print("Tool Result:")
            print(result)

            # نرجع نتيجة الـTool للـLLM
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result, default=int)
                }
            )
            print("Sending tool result back to LLM...")
#Test
result=run_agent("ORD-9999")
print(result)

    